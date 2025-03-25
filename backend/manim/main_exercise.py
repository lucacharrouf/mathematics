from dotenv import load_dotenv
import os
import argparse
import requests
import json
import re
import traceback
from generate_video_exercise import VideoGenerator
from prompts_exercise import process_math_visualization_request
from enum import Enum
import time
from tenacity import retry, stop_after_attempt, wait_exponential

class MacroTopic(Enum):
    LINEAR_ALGEBRA = "linear algebra"
    PROBABILITY = "probability"
    CALCULUS = "calculus"

class ProblemType(Enum):
    CONCEPT = "concept"
    EXERCISE = "exercise"

def validate_macro_topic(value):
    """Validate that the macro topic is one of the allowed values."""
    try:
        value = value.lower()
        if value not in [topic.value for topic in MacroTopic]:
            raise argparse.ArgumentTypeError(
                f"Invalid macro topic. Must be one of: {', '.join([topic.value for topic in MacroTopic])}"
            )
        return value
    except AttributeError:
        raise argparse.ArgumentTypeError("Macro topic must be a string")

def validate_problem_type(value):
    """Validate that the problem type is one of the allowed values."""
    try:
        value = value.lower()
        if value not in [ptype.value for ptype in ProblemType]:
            raise argparse.ArgumentTypeError(
                f"Invalid problem type. Must be one of: {', '.join([ptype.value for ptype in ProblemType])}"
            )
        return value
    except AttributeError:
        raise argparse.ArgumentTypeError("Problem type must be a string")

def create_safe_filename(topic, problem_type):
    """Create a safe filename from topic and problem type."""
    if problem_type == "exercise":
        # For exercises, try to extract the main mathematical concept
        math_terms = {
            'vector': ['vector', 'projection', 'orthogonal', 'parallel', 'perpendicular', 'span'],
            'matrix': ['matrix', 'determinant', 'eigenvalue', 'eigenvector', 'linear'],
            'function': ['function', 'derivative', 'integral', 'limit'],
            'probability': ['probability', 'distribution', 'random', 'expected'],
            'calculus': ['derivative', 'integral', 'limit', 'differential']
        }
        
        # Try to find the main concept
        found_terms = []
        for concept, terms in math_terms.items():
            if any(term in topic.lower() for term in terms):
                found_terms.append(concept)
                # Add the specific term that was found
                specific_terms = [term for term in terms if term in topic.lower()]
                found_terms.extend(specific_terms)
        
        if found_terms:
            # Use the first main concept and up to 2 specific terms
            safe_name = '_'.join(dict.fromkeys(found_terms[:3]))  # Remove duplicates
        else:
            # If no mathematical terms found, use first few words
            words = [w for w in topic.split()[:3] if len(w) > 2]  # Skip small words
            safe_name = '_'.join(words)
    else:
        # For concepts, use the topic directly but clean it
        safe_name = '_'.join(topic.split()[:3])

    # Clean the filename
    safe_name = safe_name.lower()
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)  # Remove special characters
    safe_name = re.sub(r'[-\s]+', '_', safe_name)   # Replace spaces/hyphens with underscore
    safe_name = re.sub(r'_+', '_', safe_name)       # Remove multiple underscores
    
    return f"generated_{safe_name[:50]}"  # Limit length to 50 chars

def validate_topic_content(code, topic):
    """Enhanced validation for topic-specific content."""
    topic_keywords = {
        'eigenvalues': ['eigenvalue', 'eigenvector', 'linear_transform', 'matrix', 'scaling', 'Av=λv'],
        'vector': ['vector', 'arrow', 'direction', 'magnitude', 'Vector'],
        'matrix': ['matrix', 'transform', 'linear', 'multiplication', 'Matrix'],
        'probability': ['probability', 'random', 'distribution', 'expected', 'sample'],
        'calculus': ['derivative', 'integral', 'limit', 'differential', 'rate']
    }
    
    # Convert topic to lowercase for comparison
    topic_lower = topic.lower()
    
    # Find the most relevant keyword set
    keywords = []
    for key, values in topic_keywords.items():
        if key in topic_lower:
            keywords = values
            break
    
    if not keywords:
        # If no specific keywords found, use the topic words as keywords
        keywords = [word.lower() for word in topic.split() if len(word) > 2]
    
    # Check for presence of keywords and class name
    matches = sum(1 for keyword in keywords if keyword.lower() in code.lower())
    class_name_present = topic.lower().replace(' ', '') in code.lower()
    
    # Require at least 2 keyword matches and proper class name
    return (matches >= 2 and class_name_present), matches, keywords

def extract_code_from_response(response):
    """Extract code between CODE_START and CODE_END tags."""
    pattern = r'<CODE_START>\s*(.*?)\s*</CODE_END>'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def generate_code_with_validation(topic, video_gen, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            # Simplified, more direct prompt
            prompt = f"""
            Generate Manim code for visualizing {topic}. 
            
            Requirements:
            1. The code MUST be about {topic}
            2. The Scene class MUST be named '{topic.replace(' ', '')}Scene'
            3. Use appropriate Manim objects and methods
            
            Format your response EXACTLY like this:
            <CODE_START>
            from manim import *

            class {topic.replace(' ', '')}Scene(Scene):
                def construct(self):
                    # Your code here
            </CODE_START>
            """
            
            response = video_gen.generator._send_prompt(prompt)
            
            # Extract code between tags
            code = extract_code_from_response(response)
            if not code:
                print(f"❌ Attempt {attempt + 1}: No code found between tags")
                continue
            
            # Validate the code content
            is_valid, matches, keywords = validate_topic_content(code, topic)
            if is_valid:
                print(f"✓ Code validation successful ({matches} keyword matches)")
                return code
            else:
                print(f"❌ Attempt {attempt + 1}: Code validation failed")
                print(f"Expected keywords: {keywords}")
                
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            
    return None

class CodeGenerationError(Exception):
    """Custom exception for code generation failures."""
    pass

def main():
    # Parse command-line arguments with the new structure
    parser = argparse.ArgumentParser(description="Generate Manim animations for math concepts")
    parser.add_argument(
        "--topic", 
        type=str, 
        required=True, 
        help="Specific mathematical topic to animate"
    )
    parser.add_argument(
        "--macro-topic", 
        type=validate_macro_topic, 
        required=True,
        help="Main topic area (linear algebra, probability, or calculus)"
    )
    parser.add_argument(
        "--problem-type", 
        type=validate_problem_type, 
        required=True,
        help="Type of problem (concept or exercise)"
    )
    parser.add_argument(
        "--server-url", 
        type=str, 
        default="http://localhost:4000",
        help="URL of the Node.js server"
    )
    args = parser.parse_args()
    
    print(f"Server URL: {args.server_url}")
    
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please create a .env file with your API key or set it as an environment variable")
        return
    
    # Initialize the video generator
    video_gen = VideoGenerator(api_key=api_key)

    print("\n" + "="*50)
    print("STARTING VISUALIZATION PROCESS")
    print("="*50)
    print(f"Topic requested: '{args.topic}'")
    print(f"Macro topic: '{args.macro_topic}'")
    print(f"Problem type: '{args.problem_type}'")
    print(f"Using prompts from: {'concept_prompts.py' if args.problem_type == 'concept' else 'exercise_prompts.py'}")
    print("-"*50)

    # Define the LLM response function that will be used by process_math_visualization_request
    @retry(stop=stop_after_attempt(5), 
           wait=wait_exponential(multiplier=1, min=4, max=30))
    def get_llm_response(prompt):
        try:
            print("\nSending prompt to AI model...")
            print("Prompt type:", end=" ")
            if "TOPIC_EXTRACTION" in prompt:
                print("ANALYZING QUERY TYPE (Exercise/Concept/Visualization)")
            elif "CONCEPT_BREAKDOWN" in prompt:
                print("BREAKING DOWN MATHEMATICAL CONCEPT")
            elif "DESIGN" in prompt:
                print("DESIGNING ANIMATION")
            elif "ANIMATION_TESTING" in prompt:
                print("TESTING ANIMATION DESIGN")
            elif "CODE_GENERATION" in prompt:
                print("GENERATING MANIM CODE")
            else:
                print("OTHER")
            
            response = video_gen.generator._send_prompt(prompt)
            print("Response received!")
            return response
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            raise  # Re-raise the exception to trigger retry

    print("\nSTEP 1: ANALYZING QUERY")
    print("-"*50)
    visualization_result = process_math_visualization_request(
        query=args.topic,
        macro_topic=args.macro_topic,
        problem_type=args.problem_type,
        get_llm_response_func=get_llm_response
    )

    if not visualization_result['success']:
        print("\n❌ VISUALIZATION REQUEST FAILED")
        print(f"Error: {visualization_result.get('error', 'Unknown error')}")
        return

    print("\nSTEP 2: EXTRACTING RESULTS")
    print("-"*50)
    code = visualization_result['code']
    topic = visualization_result['topic']
    animation_design = visualization_result['animation_design']
    scene_plan = visualization_result.get('scene_plan', '')  # Add scene plan

    print(f"Extracted topic: '{topic}'")
    print(f"Animation design length: {len(animation_design) if animation_design else 0} characters")
    print(f"Scene plan length: {len(scene_plan) if scene_plan else 0} characters")
    print(f"Generated code length: {len(code) if code else 0} characters")

    if code:
        print("\nSTEP 3: SAVING CODE AND GENERATING VIDEO")
        print("-"*50)
        
        # Create safe filename
        safe_filename = create_safe_filename(args.topic, args.problem_type)
        code_filename = f"{safe_filename}.py"
        code_path = os.path.join(video_gen.code_dir, code_filename)
        
        try:
            # Save the code from visualization_result
            print(f"Creating code file: {code_filename}")
            os.makedirs(os.path.dirname(code_path), exist_ok=True)
            with open(code_path, 'w') as f:
                f.write(code)
            print(f"✓ Code saved successfully")

            print("\nSTEP 4: GENERATING ANIMATION")
            print("-"*50)
            print("Running Manim to generate video...")
            result = video_gen.generate_video_from_code(code_path, args.topic)
            
            if isinstance(result, str):
                success = True
                print("✓ Video generated successfully!")
                
                # Save artifacts
                artifacts_dir = os.path.join(video_gen.videos_dir, f"{safe_filename}_artifacts")
                os.makedirs(artifacts_dir, exist_ok=True)

                print("\nSTEP 5: SAVING ARTIFACTS")
                print("-"*50)
                print(f"Saving artifacts to: {artifacts_dir}")
                
                with open(os.path.join(artifacts_dir, "animation_design.txt"), 'w') as f:
                    f.write(animation_design)
                print("✓ Saved animation design")
                print(f"✓ All artifacts saved to: {artifacts_dir}")
            else:
                success = False
                print("❌ Video generation failed")

            # Save to database (single attempt)
            print("\nSTEP 6: SAVING TO DATABASE")
            print("-"*50)
            data = {
                "topic": args.topic,
                "macroTopic": args.macro_topic,
                "problemType": args.problem_type,
                "code": code,
                "status": "completed" if success else "failed",
                "videoPath": result if success and isinstance(result, str) else "",
                "animationDesign": animation_design
            }
            
            print("Sending data to database...")
            endpoint_url = f"{args.server_url}/videos/save-from-python"
            response = requests.post(
                endpoint_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 201:
                print("✓ Successfully saved to database")
            else:
                print(f"❌ Failed to save to database (Status: {response.status_code})")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            traceback.print_exc()
            success = False
            result = None

        print("\n" + "="*50)
        print("PROCESS COMPLETE")
        print("="*50)
        if success:
            print(f"✓ Successfully created visualization for: '{args.topic}'")
            print(f"✓ Video saved to: {result}")
        else:
            print(f"❌ Failed to create visualization for: '{args.topic}'")
        print("="*50 + "\n")
    else:
        print("\n❌ CODE GENERATION FAILED")
        print("No code was generated")

if __name__ == "__main__":
    main()