from dotenv import load_dotenv
import os
import argparse
import requests
import json
import re
import traceback
from generate_video_exercise import VideoGenerator
from prompts_test_ic_enhanced import (
    VIDEO_IDEA_GENERATOR_SYSTEM_PROMPT, 
    VIDEO_IDEA_GENERATOR_USER_PROMPT,
    SCENE_PLANNER_SYSTEM_PROMPT,
    SCENE_PLAN_USER_PROMPT,
    SCENE_EVALUATOR_SYSTEM_PROMPT,
    SCENE_EVALUATION_USER_PROMPT,
    CODE_GENERATOR_SYSTEM_PROMPT,
    CODE_GENERATOR_USER_PROMPT,
    CODE_LAYOUT_EVALUATOR_SYSTEM_PROMPT,
    CODE_LAYOUT_EVALUATION_USER_PROMPT,
    evaluate_and_fix_layout,
    validate_and_fix_manim_code,
    enforce_boundary_checks,
    generate_key_takeaways,
    KEY_TAKEAWAYS_SYSTEM_PROMPT,
    KEY_TAKEAWAYS_USER_PROMPT
)
import time
from tenacity import retry, stop_after_attempt, wait_exponential

def create_safe_filename(topic, suffix="_ic"):
    """Create a safe filename from the topic with optional suffix.
    
    Args:
        topic: The topic to use in the filename
        suffix: Optional suffix to add after the topic name
    
    Returns:
        A safe filename with the topic name and suffix
    """
    # Clean the filename
    safe_name = topic.lower()
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)  # Remove special characters
    safe_name = re.sub(r'[-\s]+', '_', safe_name)   # Replace spaces/hyphens with underscore
    safe_name = re.sub(r'_+', '_', safe_name)       # Remove multiple underscores
    
    return f"{safe_name[:40]}{suffix}"  # Limit topic length to 40 chars + suffix

def extract_code_from_response(response):
    """Extract code between python tags."""
    pattern = r'```python\s*(.*?)\s*```'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def validate_and_fix_manim_code(code):
    """Perform basic validation and fixes on Manim code before saving."""
    if not code:
        return None
        
    # Check for critical errors
    critical_issues = []
    
    # 1. Check for proper import
    if not re.search(r'from\s+manim\s+import', code):
        critical_issues.append("Missing manim imports")
        code = "from manim import *\n\n" + code
    
    # 2. Check for class definition
    if not re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', code):
        critical_issues.append("Missing Scene class definition")
    
    # 3. Check for construct method
    if not re.search(r'def\s+construct\s*\(\s*self\s*\)', code):
        critical_issues.append("Missing construct method")
    
    if critical_issues:
        print("⚠️ Issues in generated code (attempting fixes):")
        for issue in critical_issues:
            print(f"  - {issue}")
    
    # Ensure imports are complete
    if 'from manim import' in code and 'from manim import *' not in code:
        code = code.replace('from manim import', 'from manim import *')
        print("✓ Fixed incomplete import statement")
    
    # Apply additional fixes: Comment any plain text lines
    lines = code.split('\n')
    fixed_lines = []
    in_function_def = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines or already commented lines
        if not stripped or stripped.startswith('#'):
            fixed_lines.append(line)
            continue
        
        # Track if we're in a function definition
        if re.match(r'\s*def\s+', line):
            in_function_def = True
        
        # Check if line looks like a descriptive text without code elements
        if in_function_def and not any(char in stripped for char in "={}[](),.+-*/:'\"\\"):
            # Comment it as descriptive text
            leading_space = len(line) - len(line.lstrip())
            fixed_lines.append(' ' * leading_space + '# ' + stripped)
            print(f"⚠️ Line {i+1}: Commented text '{stripped}'")
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate Manim animations for math concepts")
    parser.add_argument(
        "--topic", 
        type=str, 
        required=True, 
        help="Mathematical topic to animate"
    )
    parser.add_argument(
        "--server-url", 
        type=str, 
        default="http://localhost:4000",
        help="URL of the Node.js server"
    )
    args = parser.parse_args()
    
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
    print("Using simplified prompts from prompts_test_ic.py")
    print("-"*50)
    
    # Define the LLM response function
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_llm_response(system_prompt, user_prompt):
        try:
            print("\nSending prompt to AI model...")
            # Combine system and user prompts into a single message
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = video_gen.generator._send_prompt(combined_prompt)
            print("Response received!")
            return response
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            raise  # Re-raise the exception to trigger retry
    
    try:
        # Step 1: Generate video ideas
        print("\nSTEP 1: GENERATING VIDEO IDEAS")
        print("-"*50)
        
        video_ideas_response = get_llm_response(
            system_prompt=VIDEO_IDEA_GENERATOR_SYSTEM_PROMPT,
            user_prompt=VIDEO_IDEA_GENERATOR_USER_PROMPT.format(video_prompt=args.topic)
        )
        
        # Parse video ideas - we'll assume the response is the full set of scene descriptions
        scenes = video_ideas_response.strip().split('\n\n')
        
        # Keep only unique, non-empty scenes
        scenes = [scene.strip() for scene in scenes if scene.strip()]
        scenes = [scene for scene in scenes if len(scene) > 20]  # Minimal length check
        
        if not scenes:
            print("❌ Failed to generate scene ideas")
            return
        
        print(f"✓ Generated {len(scenes)} scene ideas")
        for i, scene in enumerate(scenes):
            print(f"\nScene {i+1}: {scene[:100]}...")
        
        # We'll just use the first scene for this test
        selected_scene = scenes[0]
        
        # Step 2: Plan the scene in detail
        print("\nSTEP 2: PLANNING SCENE IN DETAIL")
        print("-"*50)
        
        scene_plan_response = get_llm_response(
            system_prompt=SCENE_PLANNER_SYSTEM_PROMPT,
            user_prompt=SCENE_PLAN_USER_PROMPT.format(scene_prompt=selected_scene)
        )
        
        scene_plan = scene_plan_response.strip()
        if not scene_plan:
            print("❌ Failed to generate scene plan")
            return
        
        print(f"✓ Generated scene plan ({len(scene_plan)} characters)")
        print(f"\nScene plan preview: {scene_plan[:200]}...")
        
        # Step 3: Evaluate the scene plan
        print("\nSTEP 3: EVALUATING SCENE PLAN")
        print("-"*50)
        
        evaluation_response = get_llm_response(
            system_prompt=SCENE_EVALUATOR_SYSTEM_PROMPT,
            user_prompt=SCENE_EVALUATION_USER_PROMPT.format(scene_plan=scene_plan)
        )
        
        # Check if there are issues that need to be fixed
        if "does not meet the criteria" in evaluation_response.lower():
            print("⚠️ Scene plan evaluation found issues, regenerating plan...")
            
            # Regenerate the scene plan with the evaluation feedback
            improved_prompt = f"""
            Your previous scene plan had some issues:
            
            {evaluation_response}
            
            Please create an improved scene plan for this scene:
            
            {selected_scene}
            """
            
            scene_plan_response = get_llm_response(
                system_prompt=SCENE_PLANNER_SYSTEM_PROMPT,
                user_prompt=improved_prompt
            )
            
            scene_plan = scene_plan_response.strip()
            print(f"✓ Generated improved scene plan ({len(scene_plan)} characters)")
        else:
            print("✓ Scene plan meets all criteria")
        
        # Step 4: Generate Manim code
        print("\nSTEP 4: GENERATING MANIM CODE")
        print("-"*50)
        
        code_response = get_llm_response(
            system_prompt=CODE_GENERATOR_SYSTEM_PROMPT,
            user_prompt=CODE_GENERATOR_USER_PROMPT.format(code_spec=scene_plan)
        )
        
        # Extract code from response (between ```python tags)
        code = extract_code_from_response(code_response)
        
        if not code:
            print("❌ Failed to extract code from response")
            print("Response preview:", code_response[:200])
            return
        
        # First, do basic validation and fixes
        fixed_code = validate_and_fix_manim_code(code)
        if fixed_code:
            code = fixed_code
        
        # Now, evaluate and fix layout issues
        print("\nSTEP 4a: EVALUATING CODE LAYOUT")
        print("-"*50)
        layout_fixed_code = evaluate_and_fix_layout(code, get_llm_response)
        if layout_fixed_code:
            code = layout_fixed_code
            print("✓ Applied layout optimization")
        
        # Add boundary enforcement
        print("\nSTEP 4b: ADDING BOUNDARY CHECKS")
        print("-"*50)
        boundary_checked_code = enforce_boundary_checks(code)
        if boundary_checked_code != code:
            code = boundary_checked_code
            print("✓ Added boundary safety checks to ensure text stays within frame")
            print("   • Added safe_position utility function")
            print("   • Added background rectangles for text")
            print("   • Added automatic zone positioning (TOP/MIDDLE/BOTTOM)")
        
        print(f"✓ Generated Manim code ({len(code)} characters)")
        
        # Create class name for the code
        safe_title = ''.join(c for c in args.topic if c.isalnum() or c.isspace())
        class_name = ''.join(word.capitalize() for word in safe_title.split()) + 'Scene'
        
        # Make sure the code uses the correct class name
        if f"class {class_name}" not in code:
            old_class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
            if old_class_match:
                old_class_name = old_class_match.group(1)
                code = code.replace(f"class {old_class_name}", f"class {class_name}")
                print(f"✓ Renamed class from {old_class_name} to {class_name}")
        
        # Step 5: Save the code and generate the video
        print("\nSTEP 5: SAVING CODE AND GENERATING VIDEO")
        print("-"*50)
        
        # Create safe filename with _ic suffix
        safe_filename = create_safe_filename(args.topic, "_ic")
        code_filename = f"{safe_filename}.py"
        code_path = os.path.join(video_gen.code_dir, code_filename)
        
        # Save the code
        print(f"Creating code file: {code_filename}")
        os.makedirs(os.path.dirname(code_path), exist_ok=True)
        with open(code_path, 'w') as f:
            f.write(code)
        print(f"✓ Code saved successfully as {code_filename}")
        
        # After code generation and before running the animation
        # Add a final code validation step
        print("\nSTEP 4c: FINAL CODE VALIDATION")
        print("-"*50)
        
        # Basic syntax check - make sure there are no \1, \2, etc.
        if re.search(r'\\[0-9]', code):
            print("⚠️ Found invalid escape sequences in the code - fixing...")
            code = re.sub(r'\\[0-9]', '', code)
            with open(code_path, 'w') as f:
                f.write(code)
            print("✓ Fixed escape sequence issues")
        
        # Add after the final code validation step in main_test_ic.py
        print("\nSTEP 4d: FIXING COORDINATE DIMENSIONS")
        print("-"*50)
        
        # Read the current code
        with open(code_path, 'r') as f:
            current_code = f.read()
        
        # Fix for 2D coordinates in Dot creation
        if "_coords" in current_code and "Dot(" in current_code:
            print("⚠️ Checking for 2D coordinates in Dot objects...")
            
            # First approach: Convert 2D coordinate arrays to 3D
            coord_pattern = r'(\w+_coords\s*=\s*\[(?:\s*\([^)]+\)\s*,?)+\])'
            for match in re.finditer(coord_pattern, current_code):
                coords_def = match.group(1)
                # Check if we have 2D coordinates (no third component)
                if re.search(r'\(\s*-?\d+\.?\d*\s*,\s*-?\d+\.?\d*\s*\)', coords_def):
                    print(f"⚠️ Found 2D coordinates in: {coords_def[:50]}...")
                    # Replace with 3D coordinates by adding ,0 as the z-coordinate
                    fixed_coords = re.sub(
                        r'\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)',
                        r'(\1, \2, 0)',
                        coords_def
                    )
                    current_code = current_code.replace(coords_def, fixed_coords)
                    print("✓ Fixed coordinates to 3D format")
            
            # Second approach: Modify Dot creation to handle 2D points
            if re.search(r'Dot\(\s*\w+\s*[,)]', current_code) and "import numpy as np" not in current_code:
                print("⚠️ Adding numpy import for coordinate handling")
                current_code = current_code.replace("from manim import *", "from manim import *\nimport numpy as np")
            
            dot_pattern = r'(Dot\(\s*)(\w+)(\s*,|\s*\))'
            for match in re.finditer(dot_pattern, current_code):
                full_match = match.group(0)
                prefix = match.group(1)
                point_var = match.group(2)
                suffix = match.group(3)
                
                # Only apply to point variables that are likely coordinates
                if point_var.endswith("_coords") or point_var == "point":
                    continue  # Skip list variables - we handle these in the loop
                
                if "_coords" in current_code and f"for {point_var} in" in current_code:
                    # For loop variable from coords
                    print(f"⚠️ Fixing Dot creation with loop variable: {point_var}")
                    replacement = f"{prefix}np.array([{point_var}[0], {point_var}[1], 0]){suffix}"
                    current_code = current_code.replace(full_match, replacement)
                    print(f"✓ Fixed Dot creation: {full_match} → {replacement}")
            
            # Save the updated code
            with open(code_path, 'w') as f:
                f.write(current_code)
            print("✓ Saved coordinate dimension fixes to file")
        
        # Check for commented z-coordinates
        print("\nChecking for commented z-coordinates...")
        with open(code_path, 'r') as f:
            current_code = f.read()

        # Fix commented out z-coordinates in move_to calls
        if re.search(r'move_to\(\s*\[\s*[^,\]]+,\s*[^,\]]+,?\s*(?:#\s*0)?\s*\]\s*\)', current_code):
            print("⚠️ Found move_to() calls with missing z-coordinate")
            fixed_code = re.sub(
                r'move_to\(\s*\[\s*([^,\]]+),\s*([^,\]]+),?\s*(?:#\s*0)?\s*\]\s*\)',
                r'move_to([\1, \2, 0])',
                current_code
            )
            
            # Fix other potential cases
            fixed_code = re.sub(
                r'(\w+\.move_to\(\[)([^,\]]+),\s*([^,\]]+)(\s*\]\))',
                r'\1\2, \3, 0\4',
                fixed_code
            )
            
            with open(code_path, 'w') as f:
                f.write(fixed_code)
            print("✓ Fixed missing z-coordinates")
        
        # Generate the video
        print("\nRunning Manim to generate video...")
        result = video_gen.generate_video_from_code(code_path, args.topic)
        
        if isinstance(result, str) and os.path.exists(result):
            # If successful, rename the video file to include _ic suffix
            success = True
            print("✓ Video generated successfully!")
            
            # Get the directory and base filename
            video_dir = os.path.dirname(result) # backend/backend/manim/content/videos_dir/
            video_filename = os.path.basename(result)
            
            # Add _ic before the extension if it's not already there
            if "_ic" not in video_filename:
                name, ext = os.path.splitext(video_filename)
                new_filename = f"{name}_ic{ext}"
                new_path = os.path.join(video_dir, new_filename)
                
                try:
                    os.rename(result, new_path)
                    print(f"✓ Renamed video file to include _ic suffix: {new_filename}")
                    result = new_path  # Update result to the new path
                except Exception as e:
                    print(f"⚠️ Warning: Could not rename video file: {e}")
            
            # Save artifacts
            artifacts_dir = os.path.join(video_gen.videos_dir, f"{safe_filename}_artifacts")
            os.makedirs(artifacts_dir, exist_ok=True)
            
            print("\nSTEP 6: SAVING ARTIFACTS")
            print("-"*50)
            print(f"Saving artifacts to: {artifacts_dir}")
            
            with open(os.path.join(artifacts_dir, "scene_plan.txt"), 'w') as f:
                f.write(scene_plan)
            print("✓ Saved scene plan")
            
            # Add a new step to generate key takeaways
            print("\nSTEP 6a: GENERATING KEY TAKEAWAYS")
            print("-"*50)
            
            # Get the key takeaways
            key_takeaways = generate_key_takeaways(args.topic, get_llm_response)
            
            print("✓ Generated key takeaways:")
            print(key_takeaways)
            
            # Save the key takeaways to a file
            with open(os.path.join(artifacts_dir, "key_takeaways.txt"), 'w') as f:
                f.write(key_takeaways)
            print("✓ Saved key takeaways to file")
            
            # Save to database
            print("\nSTEP 7: SAVING TO DATABASE")
            print("-"*50)
            
            # Create a video path that includes the video name after videos_dir/
            video_name = os.path.splitext(os.path.basename(result))[0]  # Get filename without extension
            custom_video_path = f"backend/manim/content/videos_dir/{os.path.basename(result)}"
            
            # Ensure key takeaways are properly formatted (remove any leading/trailing whitespace)
            key_takeaways = key_takeaways.strip()
            
            data = {
                "topic": args.topic,
                "code": code,
                "status": "completed" if success else "failed",
                "videoPath": custom_video_path if success and isinstance(result, str) else "",
                "scenePlan": scene_plan,
                "keyTakeaways": key_takeaways
            }
            
            print(f"Video path to be saved in DB: {custom_video_path}")
            print(f"Key takeaways length: {len(key_takeaways)} characters")
            print(f"Key takeaways preview: {key_takeaways[:100]}...")
            
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
        else:
            success = False
            print("❌ Video generation failed")
        
        print("\n" + "="*50)
        print("PROCESS COMPLETE")
        print("="*50)
        if success:
            print(f"✓ Successfully created visualization for: '{args.topic}'")
            print(f"✓ Video saved to: {result}")
        else:
            print(f"❌ Failed to create visualization for: '{args.topic}'")
        print("="*50 + "\n")
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 