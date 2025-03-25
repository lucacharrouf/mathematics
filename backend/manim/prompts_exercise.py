import re
from manim import UP, DOWN, RIGHT, VGroup, SurroundingRectangle, BLACK, WHITE
from concept_prompts import CONCEPT_EXTRACTION, CONCEPT_DESIGN
from exercise_prompts import EXERCISE_EXTRACTION, EXERCISE_DESIGN
# =============================================================================
# Core Prompts for Manim Animation Generation
# =============================================================================

# Pre-processing stage to extract core concept from complex queries
TOPIC_EXTRACTION = '''You are a math professor at MIT specialized in interpreting mathematical queries and exercises. 
Your task is to extract the core concept that needs visualization.

<original_query>
{original_query}
</original_query>

First, determine if this is a specific exercise, a conceptual question, or a visualization request.

# This should be taken out and classifier without the use of claude API
<query_analysis>
Query type: [Exercise / Concept / Visualization request]
Subject area: [e.g., Linear Algebra, Statistics, Calculus, etc.]
Core visualization needs: [List the key mathematical ideas that would benefit from visualization]
</query_analysis>

<extracted_topic>
Based on your analysis, provide a clear, concise statement of what should be visualized. This should be a fundamental mathematical concept, not the entire exercise.
</extracted_topic>

<visualization_scope>
Identify specifically what aspects of this topic should be visualized:
1. [Key aspect 1]
2. [Key aspect 2]
3. [Key aspect 3]
</visualization_scope>
'''

# Enhanced concept breakdown with original query context
CONCEPT_BREAKDOWN = '''You are a math professor at MIT specializing in breaking down mathematical concepts for visualization. 
Before designing an animation, you need to analyze the concept and identify the best approach to visualize it.

<math_topic>
{topic}
</math_topic>

<original_query>
{original_query}
</original_query>

<audience>
{audience_level}
</audience>

First, identify the underlying mathematical concepts that need visualization:

<concept_identification>
Core mathematical concept(s): [List the 1-3 primary concepts]
Related sub-concepts: [List supporting concepts]
Visualization goal: [What insight should the visualization provide]
</concept_identification>

Analyze this mathematical concept and break it down into visualizable components:

<concept_analysis>
1. Core Definition: [Provide a clear, concise definition of the concept]

2. Key Components: [List the essential sub-concepts or elements that make up this concept]

3. Intuitive Understanding: [Describe how this concept can be understood intuitively, using analogies or real-world examples]

4. Common Misconceptions: [Identify misconceptions or learning obstacles associated with this concept]

5. Visual Representation Options: [List 3-5 different ways this concept could be visualized, from concrete to abstract]

6. Progressive Learning Path: [Outline a step-by-step progression for introducing this concept visually]

7. Related Concepts: [Identify related concepts that might help provide context]

8. Applications: [Briefly describe where this concept is applied in the real world]

9. Connection to Original Query: [Explain how this visualization will specifically help understand the original question or exercise]
</concept_analysis>

<visualization_approach>
Based on the analysis above, recommend the most effective approach for visualizing this concept in a 30-second animation. 
Explain why this approach would be most effective for building understanding, specifically in the context of the original query.
</visualization_approach>

<key_visual_elements>
List the specific visual elements that should be included in the animation to effectively convey this concept:
1. [Element 1 with justification]
2. [Element 2 with justification]
3. [Element 3 with justification]
...
</key_visual_elements>
'''

# Enhanced animation design prompt
DESIGN = '''You are an expert scene planning for mathematical visualizations. 
You have strong visual taste and know how to create visualisations that allow people to understand complex topics. 

Your task is to design a 30-45 second animation explaining a mathematical concept.

Part 1: Animation Design

<math_topic>
{topic}
</math_topic>

<original_query>
{original_query}
</original_query>

<audience>
{audience_level}
</audience>

Your goal is to create a clear, well-paced animation that explains this concept. Follow these STRICT guidelines:

1. Scene Structure (30-45 seconds total):
   - Introduction (5-7 seconds): Present the topic clearly
   - Main Content (20-30 seconds): Break down into distinct scenes
   - Summary (5-8 seconds): Key takeaways

2. Scene Clarity Rules:
   - ONE main idea per scene
   - NO MORE than 3-4 elements visible at once
   - Clear transitions between scenes using text slides
   - Black background for better visibility
   - Generous spacing between elements

3. Timing and Pacing:
   - Each new element appears with a 1-2 second pause
   - Text remains visible for at least 3-4 seconds
   - Scene transitions use fade effects (2 seconds)
   - Allow time for understanding (no rushing)

4. Scene Transitions:
   - Use clear text slides between major concepts
   - Fade to black between scenes (1.5 seconds)
   - Show transition text for 2-3 seconds
   - Keep transition text simple and descriptive

5. Final Summary Requirements:
   - Title: "Key Points to Remember:"
   - 3-4 bullet points maximum
   - One-line summary per point
   - Keep visible for 5-8 seconds
   - Use emphasis for important terms

<pedagogy_principles>
Follow these educational design principles:
1. Start with concrete examples before abstract concepts
2. Use visual metaphors that connect to everyday experiences
3. Keep each scene focused on ONE clear idea
4. Allow sufficient processing time between concepts
5. Use consistent visual language throughout
6. Include clear scene transitions
7. End with memorable key points
8. Maintain visual simplicity
</pedagogy_principles>

After your planning, provide your animation description in this format:

<animation_design>
<scene_breakdown>
[List each scene with its duration and main focus]
Scene 1 (X seconds): [Purpose]
Scene 2 (X seconds): [Purpose]
...
Transition Slides: [List the text for each transition]
Summary Scene (X seconds): [Key points to remember]
</scene_breakdown>

<scene_description>
[Detailed description of each scene, including:
- Exact text and equations to show
- Clear spacing and positioning
- Timing for each element
- Transition descriptions]
</scene_description>

<key_takeaways>
1. [First key point to remember]
2. [Second key point to remember]
3. [Third key point to remember]
</key_takeaways>
</animation_design>

<self_evaluation>
[Evaluate the design considering:
- Scene clarity and simplicity
- Pacing and timing
- Effectiveness of transitions
- Memorability of key points
- Overall learning experience]
</self_evaluation>
'''

# Enhanced animation testing prompt
ANIMATION_TESTING = '''You are an AI assistant specializing in evaluating mathematical animations.
You'll review a proposed animation design and identify potential issues before implementation.

<math_topic>
{topic}
</math_topic>

<original_query>
{original_query}
</original_query>

<animation_design>
{animation_design}
</animation_design>

Evaluate this animation design by simulating how different viewers would experience it:

<novice_viewer>
Analyze how a novice in this mathematical area would experience this animation:
- What concepts might they struggle to follow?
- Which visual elements might be confusing?
- What prior knowledge is the animation assuming they have?
- What questions might they still have after watching?
</novice_viewer>

<expert_viewer>
Analyze how a subject matter expert would view this animation:
- What important nuances or details are missing?
- Are there any technical inaccuracies?
- Does the animation oversimplify important aspects?
- What additional depth could be added without overwhelming novices?
</expert_viewer>

<query_relevance>
Evaluate how well the animation addresses the specific needs of the original query:
- Does it visualize the key concepts needed to understand the query?
- Are there any gaps between what's visualized and what needs to be understood?
- Would this animation help someone make progress on the original problem or question?
</query_relevance>

<cognitive_load_analysis>
Analyze the cognitive load of this animation:
- Identify moments where too much information is presented at once
- Note any concepts that need more time to process
- Suggest ways to chunk information more effectively
- Identify visual elements that might distract from the main concept
</cognitive_load_analysis>

<design_improvements>
Based on your analysis, suggest specific improvements to the animation design:
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]
...
</design_improvements>
'''

# Simplify the prompts to be very explicit and focused
CONCEPT_EXTRACTION = '''Create a visualization focus for {topic}.
CRITICAL: Respond EXACTLY in this format:

<visualization_focus>
[What specific aspect of {topic} should be visualized]
</visualization_focus>
'''

CONCEPT_DESIGN = '''Design a 15-second animation for {topic}.
CRITICAL: Respond EXACTLY in this format:

<animation_design>
[Frame by frame description of the animation]
</animation_design>
'''

CODE_GENERATION = '''You are an expert in the Manim python library for creating mathematical animations about {topic}.
You will write code ONLY about {topic} and nothing else.

REQUIREMENTS:
1. The code MUST be about {topic} - DO NOT change the topic!
2. Class name MUST be: {safe_class_name}
3. First line MUST be: from manim import *
4. All descriptive text must be commented with #
5. DO NOT include </CODE_START> or </CODE_END> inside your code!

CRITICAL TOPIC ENFORCEMENT:
- Your code MUST include math terminology related to {topic}
- You MUST include relevant {topic} calculations and visualization
- DO NOT create animations about other topics
- DO NOT hallucinate new topics not mentioned in the prompt

EXAMPLE STRUCTURE:
```python
from manim import *

class {safe_class_name}(Scene):
    def construct(self):
        # Setup
        title = Text("{topic}", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.5).to_edge(UP))
        
        # Main visualization specific to {topic}
        # [Your {topic} visualization code here]
```

FORMAT:
I MUST format my response with <CODE_START> followed by the code, and then </CODE_END>.
The tags are NOT part of the code - they are only markers.

<CODE_START>
from manim import *

class {safe_class_name}(Scene):
    def construct(self):
        # Your code here showing {topic}
        
        # Setup - DO NOT MODIFY THIS SECTION
        title = Text("{topic}", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.5).to_edge(UP))
        
        # Main visualization code about {topic}
</CODE_END>
'''

# =============================================================================
# Helper Functions
# =============================================================================

def validate_and_preprocess_query(query, get_llm_response_func):
    """Validate and preprocess user queries to extract visualizable concepts.
    
    Args:
        query: The user's original input query
        get_llm_response_func: Function to get LLM response for a given prompt
        
    Returns:
        Dictionary containing processed information including core topic and type
    """
    # Determine query complexity
    is_complex = len(query.split()) > 30 or "exercise" in query.lower() or "?" in query
    
    if is_complex:
        # Use topic extraction prompt to get core concept
        extraction_prompt = TOPIC_EXTRACTION.format(original_query=query)
        response = get_llm_response_func(extraction_prompt)
        
        core_topic = extract_section(response, "extracted_topic")
        visualization_scope = extract_section(response, "visualization_scope")
        
        return {
            "original_query": query,
            "core_topic": core_topic,
            "visualization_scope": visualization_scope,
            "is_complex": True
        }
    else:
        # Simple topic, use as is
        return {
            "original_query": query,
            "core_topic": query,
            "visualization_scope": None,
            "is_complex": False
        }

def extract_code_only(text, topic=None, original_query=None):
    """Extract code from between <CODE_START> and </CODE_END> tags with topic validation and fixes.
    
    Args:
        text: The response text from the API
        topic: Optional topic for validation
        original_query: Optional original query for context
        
    Returns:
        The extracted code if valid, or None if extraction failed or validation failed
    """
    if not text:
        print("Error: Empty response received")
        return None
        
    # Try standard pattern first with explicit </CODE_END> tag
    pattern = r'<CODE_START>\s*(.*?)\s*</CODE_END>'
    match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        # Try alternate pattern with </CODE_START> as closing tag (common mistake)
        pattern = r'<CODE_START>\s*(.*?)\s*</CODE_START>'
        match = re.search(pattern, text, re.DOTALL)
        
    if not match:
        # Try alternate pattern without any closing tag
        pattern = r'<CODE_START>\s*(.*?)$'
        match = re.search(pattern, text, re.DOTALL)
    
    if match:
        # Extract the code - IMPORTANT: make sure closing tags aren't included
        code = match.group(1).strip()
        
        # Remove any stray closing tags that might have been included
        code = re.sub(r'</CODE_START>|</CODE_END>', '', code)
        
        print("✓ Found code between <CODE_START> tags")
        
        # Fix 1: Verify the import statement is complete
        if not re.search(r'from\s+manim\s+import\s+\*', code):
            print("⚠️ Fixing incomplete import statement")
            code = re.sub(r'from\s+manim\s+import\s*(\n|$)', 'from manim import *\n', code)
        
        # Fix 2: Analyze lines more carefully before commenting
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines or already commented lines
            if not stripped or stripped.startswith('#'):
                fixed_lines.append(line)
                continue
            
            # Check for stray tags that need to be removed
            if stripped.startswith('<') and stripped.endswith('>'):
                print(f"⚠️ Removing tag line: {stripped}")
                continue
                
            # Don't comment these common code patterns
            if any(pattern in stripped for pattern in ['self.play(', 'self.wait(', 'return', 'import', 'class', 'def ', '=', '+', '-', '*', '/']):
                fixed_lines.append(line)
                continue
                
            # Don't comment lines that are inside parentheses, brackets, or method calls
            if any(char in stripped for pattern in ['(', ')', '{', '}', '[', ']', '.'] for char in pattern):
                fixed_lines.append(line)
                continue
                
            # Check if line is valid Python code
            try:
                compile(stripped, '<string>', 'exec')
                fixed_lines.append(line)  # Valid code, keep as is
            except SyntaxError:
                # Check if this is pure descriptive text (no code-like characters)
                if not any(keyword in stripped for keyword in ['=', '(', ')', '[', ']', '{', '}', ',', ':', '.', '+', '-', '*', '/']):
                    print(f"⚠️ Commenting descriptive text: {stripped}")
                    fixed_lines.append(f"# {stripped}")
                else:
                    # This is likely code with a syntax error
                    fixed_lines.append(line)
        
        code = '\n'.join(fixed_lines)
        
        # Final validation - check for any stray tags
        code = re.sub(r'</?CODE_[A-Z]+>|</[A-Z_]+>', '', code)
        
        # Check if the code is specifically about the requested topic
        if topic:
            # Enforce topic consistency before even checking relevance
            class_name_line = [line for line in fixed_lines if f"class {topic.replace(' ', '')}Scene" in line]
            if not class_name_line:
                print(f"⚠️ Fixing class name to match topic: {topic}")
                code = re.sub(r'class\s+\w+Scene', f"class {topic.replace(' ', '')}Scene", code)
            
            # If topic is provided, validate the code is about the topic
            if not validate_topic_relevance(code, topic, original_query):
                print(f"Warning: Extracted code does not appear to be about '{topic}'")
                # Try one last injection to make it about the requested topic
                code = enforce_topic_in_code(code, topic)
                # Validate again after fixes
                if not validate_topic_relevance(code, topic, original_query):
                    print(f"⚠️ Code still not about '{topic}' after fixes. Rejecting.")
                    return None
        
        return code
    
    print("Warning: <CODE_START> and </CODE_END> tags not found in response")
    print("First 100 chars of response:", text[:100])
    print("Last 100 chars of response:", text[-100:])
    
    # If topic validation is required, don't use fallback methods for safety
    if topic:
        print("ERROR: Strict topic validation required but <CODE_START> tags not found")
        print("Skipping fallback extraction methods for topic safety")
        return None
    
    return None

def extract_key_terms(text):
    """Extract key mathematical terms from text.
    
    Args:
        text: Text to extract terms from
        
    Returns:
        List of key terms
    """
    # Mathematical terms to look for
    math_keywords = [
        "eigenvalue", "eigenvector", "matrix", "vector", "function", "equation",
        "probability", "distribution", "derivative", "integral", "limit",
        "linear", "nonlinear", "differential", "equation", "transformation",
        "optimization", "statistic", "hypothesis", "theorem", "proof",
        "algorithm", "convergence", "series", "sequence", "maximum", "minimum",
        "likelihood", "estimation", "variance", "covariance", "correlation",
        "regression", "interpolation", "approximation", "error", "calculus",
        "algebra", "geometry", "topology", "analysis", "combinatorics",
        "graph", "set", "group", "ring", "field", "space", "manifold"
    ]
    
    # Extract terms using regex - look for mathematical notation and terms
    notation_patterns = [
        r'\\[a-zA-Z]+', # LaTeX commands
        r'[a-zA-Z]_[a-zA-Z0-9]', # Subscripts
        r'[a-zA-Z]\^[a-zA-Z0-9]', # Superscripts
        r'[a-zA-Z]\\hat', # Hat notation
        r'[a-zA-Z]\\tilde', # Tilde notation
    ]
    
    # Extract words that match math keywords
    terms = []
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in math_keywords and word not in terms:
            terms.append(word)
    
    # Extract potential mathematical notation
    for pattern in notation_patterns:
        matches = re.findall(pattern, text)
        terms.extend(matches)
    
    # Add two-word terms (like "maximum likelihood" or "linear algebra")
    two_word_terms = []
    for i in range(len(words) - 1):
        two_word = words[i] + " " + words[i+1]
        if any(keyword in two_word for keyword in math_keywords):
            two_word_terms.append(two_word)
    
    terms.extend(two_word_terms)
    return list(set(terms))  # Remove duplicates

def validate_topic_relevance(code, topic, original_query=None):
    """Check if code is relevant to the requested topic with stricter validation."""
    if not code or not topic:
        return False
    
    # Normalize the topic and create keyword variations
    topic_lower = topic.lower()
    topic_words = topic_lower.split()
    
    # Create variations of the topic keywords
    keyword_variations = set()
    keyword_variations.add(topic_lower)  # Add full topic
    keyword_variations.add(topic_lower.replace(" ", ""))  # Add without spaces
    keyword_variations.update(topic_words)  # Add individual words
    
    # Add topic-specific keywords
    topic_specific_keywords = {
        'eigenvalues': ['eigenvector', 'characteristic', 'diagonalization', 'determinant', 'λ', 'lambda'],
        'vector': ['magnitude', 'direction', 'arrow', 'component', 'projection', 'unit'],
        'matrix': ['determinant', 'inverse', 'transformation', 'linear', 'row', 'column'],
        'calculus': ['derivative', 'integral', 'limit', 'differential', 'rate', 'tangent'],
        'probability': ['random', 'distribution', 'expected', 'variance', 'sample', 'event']
    }
    
    for key, terms in topic_specific_keywords.items():
        if key in topic_lower:
            keyword_variations.update(terms)
    
    # Class name check
    class_name_pattern = f"class\\s+{topic.replace(' ', '')}Scene"
    class_name_match = re.search(class_name_pattern, code, re.IGNORECASE)
    
    # Extract text from code for keyword search
    comments = " ".join(line.split('#')[1].strip() for line in code.split('\n') 
                      if '#' in line and not line.strip().startswith('#'))
    strings = " ".join(re.findall(r'"([^"]*)"', code) + re.findall(r"'([^']*)'", code))
    
    # Check for text elements
    text_elements = re.findall(r'Text\s*\(\s*["\']([^"\']*)["\']', code)
    tex_elements = re.findall(r'Tex\s*\(\s*["\']([^"\']*)["\']', code)
    math_tex_elements = re.findall(r'MathTex\s*\(\s*["\']([^"\']*)["\']', code)
    
    # Combine all text for searching
    searchable_text = f"{comments} {strings} {' '.join(text_elements)} {' '.join(tex_elements)} {' '.join(math_tex_elements)}".lower()
    
    # Count matches and check for critical keywords
    matches = sum(1 for keyword in keyword_variations if keyword in searchable_text)
    class_name_correct = class_name_match is not None
    
    # Print debug information
    print(f"\nTopic validation for: '{topic}'")
    print(f"Class name check: {'✓' if class_name_correct else '❌'}")
    print(f"Keywords found: {[kw for kw in keyword_variations if kw in searchable_text]}")
    print(f"Total keyword matches: {matches}")
    
    # For specific critical topics, ensure specific keywords are present
    critical_topics_keywords = {
        'eigenvalues': ['eigenvalues', 'eigenvector', 'λ', 'lambda'],
        'vector projection': ['projection', 'vector', 'scalar', 'dot product'],
        'matrix multiplication': ['matrix', 'multiplication', 'product']
    }
    
    # If topic is critical, check for mandatory keywords
    for critical_topic, mandatory_keywords in critical_topics_keywords.items():
        if critical_topic in topic_lower:
            mandatory_matches = sum(1 for keyword in mandatory_keywords if keyword in searchable_text.lower())
            if mandatory_matches < 1:
                print(f"❌ Missing mandatory keywords for '{critical_topic}': {mandatory_keywords}")
                return False
    
    # Require both correct class name and sufficient keyword matches
    validation_passed = class_name_correct and matches >= 2
    if validation_passed:
        print("✓ Topic validation passed")
    else:
        print("❌ Topic validation failed")
    
    return validation_passed

def extract_section(text, section_name):
    """Extract content from a specific XML-like section or markdown headers."""
    if not text or not section_name:
        print(f"❌ Invalid input for section extraction: text={bool(text)}, section={bool(section_name)}")
        return None
        
    try:
        # First try exact XML tags
        pattern = rf'<{section_name}>(.*?)</{section_name}>'
        match = re.search(pattern, text, re.DOTALL)
        
        if not match:
            # Try markdown format with different header styles
            markdown_patterns = [
                rf'#\s*{section_name}[:\s]*\n+(.*?)(?=\n#|$)',  # # Header
                rf'##\s*{section_name}[:\s]*\n+(.*?)(?=\n##|$)',  # ## Header
                rf'###\s*{section_name}[:\s]*\n+(.*?)(?=\n###|$)',  # ### Header
                rf'\*\*{section_name}:\*\*\s*(.*?)(?=\n\*\*|\Z)',  # **Header:**
            ]
            
            for pattern in markdown_patterns:
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    break
        
        if match:
            content = match.group(1).strip()
            if content:
                # Remove markdown formatting from content
                content = re.sub(r'[#*`]', '', content)  # Remove markdown symbols
                content = re.sub(r'\n\s*-\s*', '\n', content)  # Clean bullet points
                return content
            print(f"❌ Empty content found in section: {section_name}")
        else:
            print(f"❌ Section not found: {section_name}")
            print(f"Available text (first 200 chars): {text[:200]}")
            print(f"Available text (last 200 chars): {text[-200:]}")
    except Exception as e:
        print(f"❌ Error extracting section {section_name}: {str(e)}")
    
    return None

def create_topic_safe_classname(topic):
    """Create a safe class name from a topic
    
    Args:
        topic: The topic to create a class name from
        
    Returns:
        A safe class name based on the topic
    """
    # Remove special characters and spaces
    safe_name = ''.join(c for c in topic if c.isalnum() or c.isspace())
    # Convert to CamelCase and add Scene suffix
    words = safe_name.split()
    camel_case = ''.join(word.capitalize() for word in words)
    return camel_case + 'Scene'

def format_code_generation_prompt(topic, design_scene, original_query=None):
    """Format the code generation prompt with topic-specific information
    
    Args:
        topic: The mathematical topic
        design_scene: The design specification
        original_query: The original user query for context
        
    Returns:
        Formatted prompt string
    """
    safe_class_name = create_topic_safe_classname(topic)
    
    # Handle case where original_query is None
    if original_query is None:
        original_query = topic
    
    # Replace placeholders in the prompt
    return CODE_GENERATION.format(
        topic=topic,
        design_scene=design_scene,
        safe_class_name=safe_class_name,
        original_query=original_query
    )

def validate_manim_syntax(code):
    """Check for common Manim syntax issues and deprecated methods."""
    deprecated_methods = {
        'ShowCreation': 'Create',
        'FadeInFrom': 'FadeIn',
        'FadeOutAndShift': 'FadeOut',
        'GrowFromCenter': 'Create',
        'DrawBorderThenFill': 'Create',
    }
    
    issues = []
    for old_method, new_method in deprecated_methods.items():
        if old_method in code:
            issues.append(f"Found deprecated method '{old_method}', use '{new_method}' instead")
    
    if issues:
        print("\nWarning: Found deprecated Manim syntax:")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True

def extract_code_with_retries(response, topic, get_llm_response_func, max_retries=3):
    """Extract code from response with multiple retries and explicit formatting requirements."""
    
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1} of {max_retries} to extract code")
        code = extract_code_only(response, topic)
        if code:
            print("✓ Code successfully extracted!")
            
            # Validate Manim syntax
            if not validate_manim_syntax(code):
                print("Requesting code with updated syntax...")
                enhanced_prompt = f"""Your code contains deprecated Manim methods. Please update to use current syntax:
                - Replace ShowCreation() with Create()
                - Replace FadeInFrom() with FadeIn()
                - Replace FadeOutAndShift() with FadeOut()
                - Replace GrowFromCenter() with Create()
                - Replace DrawBorderThenFill() with Create()

Previous code length: {len(code)} chars

<CODE_START>
[Your updated Manim code here]
</CODE_END>"""
                response = get_llm_response_func(enhanced_prompt)
                continue
            
            return code
            
        print(f"❌ Attempt {attempt + 1} failed to extract code")
        print("Trying again with more explicit instructions...")
        
        enhanced_prompt = f"""CRITICAL ERROR: Your previous response did not contain the required <CODE_START> and <CODE_END> tags.

Please provide ONLY the code section with the EXACT required tags:

<CODE_START>
[Your complete Manim code here]
</CODE_END>

DO NOT use markdown formatting or triple backticks. The tags must be exactly as shown above.
Previous response length: {len(response)} chars"""

        response = get_llm_response_func(enhanced_prompt)
    
    print("❌ Failed to extract code after all retry attempts")
    return None

def validate_code_format(code):
    """Validate that the code meets basic Manim requirements."""
    print("\nValidating code format...")
    required_elements = [
        ('from manim import', 'Missing manim imports'),
        ('class', 'Missing scene class definition'),
        ('Scene)', 'Scene class not properly inherited'),
        ('def construct', 'Missing construct method'),
    ]
    
    # Check for 3D-specific imports if needed
    if any(x in code for x in ['ParametricSurface', 'Surface', '3D', 'ThreeDScene']):
        required_elements.extend([
            ('from manim.mobject.three_dimensions import', 'Missing 3D object imports'),
            ('from manim.utils.space_ops import', 'Missing space operations imports')
        ])
    
    for element, error_msg in required_elements:
        if element not in code:
            print(f"❌ Validation failed: {error_msg}")
            raise ValueError(f"Invalid code format: {error_msg}")
    
    print("✓ Code format validation passed")
    return True

# =============================================================================
# Main Processing Functions
# =============================================================================

def process_math_visualization_request(query, macro_topic, problem_type, get_llm_response_func):
    """Process a mathematical visualization request based on problem type"""
    print(f"\nProcessing visualization for: {query}")
    
    try:
        # Step 1: Get visualization focus
        extraction_response = get_llm_response_func(
            CONCEPT_EXTRACTION.format(topic=query)
        )
        visualization_focus = extract_section(extraction_response, "visualization_focus")
        if not visualization_focus:
            return {"success": False, "error": "Failed to get visualization focus"}
            
        # Step 2: Get animation design
        design_response = get_llm_response_func(
            CONCEPT_DESIGN.format(topic=query)
        )
        animation_design = extract_section(design_response, "animation_design")
        if not animation_design:
            return {"success": False, "error": "Failed to get animation design"}
            
        # Step 3: Generate code
        safe_class_name = f"{query.replace(' ', '')}Scene"
        code_response = get_llm_response_func(
            CODE_GENERATION.format(
                topic=query,
                safe_class_name=safe_class_name
            )
        )
        
        # Instead, go directly to extract_code_with_retries which handles the different tag formats
        code = extract_code_with_retries(code_response, query, get_llm_response_func)
        
        if code is None:
            print("\n❌ CODE GENERATION FAILED")
            return {
                "success": False,
                "error": "Failed to generate valid code",
                "topic": query,
                "visualization_focus": visualization_focus
            }
        
        # Add final validation and fixing
        print("\nPerforming final code validation and fixes...")
        fixed_code = validate_and_fix_manim_code(code)
        
        if fixed_code is None:
            print("\n❌ FINAL CODE VALIDATION FAILED")
            return {
                "success": False,
                "error": "Code has critical issues that could not be fixed",
                "topic": query,
                "visualization_focus": visualization_focus
            }
        
        # Use the fixed code
        code = fixed_code
        
        print("\n✓ Code generation successful!")
        print(f"Generated code length: {len(code)} characters")
        
        return {
            "success": True,
            "topic": query,
            "macro_topic": macro_topic,
            "problem_type": problem_type,
            "visualization_focus": visualization_focus,
            "animation_design": animation_design,
            "code": code,
            "class_name": safe_class_name
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": False, "error": str(e)}

# Example of how to use the system (replace with your actual LLM API call)
def example_usage():
    # Define a function to get responses from your LLM API
    def get_llm_response(prompt):
        # Replace this with your actual API call
        # This is just a placeholder
        print("Sending prompt to LLM")
        return "Example response"

# Add these helper functions after the existing code

def position_text_safely(text_obj, reference_obj=None, direction=UP, buff=0.5):
    """Position text safely relative to a reference object or scene.
    
    Args:
        text_obj: The text/equation object to position
        reference_obj: The object to position relative to (optional)
        direction: The direction to offset from reference (default UP)
        buff: Buffer space between objects
    """
    if reference_obj:
        text_obj.next_to(reference_obj, direction, buff=buff)
    else:
        # If no reference, try to position at top with safe margins
        text_obj.to_edge(UP, buff=buff)

def arrange_objects_vertically(*objects, buff=0.75):
    """Arrange objects vertically with safe spacing.
    
    Args:
        *objects: The objects to arrange
        buff: Buffer space between objects
    """
    group = VGroup(*objects)
    group.arrange(DOWN, buff=buff)
    return group

def create_text_box(text_obj, buff=0.3, color=WHITE, fill_opacity=0):
    """Create a background box for text to improve visibility.
    
    Args:
        text_obj: The text object to create a box for
        buff: Padding around the text
        color: Color of the box outline
        fill_opacity: Opacity of box fill (0 for transparent)
    """
    box = SurroundingRectangle(
        text_obj,
        buff=buff,
        color=color,
        fill_color=BLACK,
        fill_opacity=fill_opacity
    )
    return VGroup(box, text_obj)

def update_text_position(text_obj, mobject):
    """Update function to keep text following a moving object.
    
    Args:
        text_obj: The text object to update
        mobject: The object to follow
    """
    def updater(text):
        text.next_to(mobject, UP, buff=0.5)
    return updater

SCENE_PLANNING = '''You are an expert manim scene planner with strong visual taste and deep understanding of mathematical visualization.

<topic>
{topic}
</topic>

CRITICAL LAYOUT RULES:
1. Screen Zones:
   - TOP ZONE (y > 2): Reserved for titles and headers only
   - MIDDLE ZONE (2 >= y >= -2): Main animation area
   - BOTTOM ZONE (y < -2): Reserved for explanatory text
   - LEFT MARGIN: Keep x < -6
   - RIGHT MARGIN: Keep x > 6

2. Text Placement:
   - All explanatory text MUST be in BOTTOM ZONE
   - Title text MUST be in TOP ZONE
   - NEVER place text over animation elements
   - Use text boxes with black background for better readability

3. Animation Space:
   - Keep main animations in MIDDLE ZONE
   - Center important transformations at (0,0)
   - Use quadrants for comparisons
   - Maximum animation width: 10 units
   - Maximum animation height: 4 units

4. Timing Rules:
   - Clear screen between major concepts
   - Wait 2 seconds after new text appears
   - Fade out all elements before new scene
   - No more than 3 elements moving simultaneously

Provide your scene plan in this EXACT format:

<scene_plan>
DURATION: [Total seconds]

SCREEN ZONES:
TOP ZONE (y > 2):
- Title placement and timing
- Section headers

MIDDLE ZONE (2 >= y >= -2):
- Animation elements and their exact coordinates
- Movement paths and transformations
- Mathematical objects (vectors, matrices, etc.)

BOTTOM ZONE (y < -2):
- Explanatory text placement
- Equation displays
- Step-by-step descriptions

FRAME-BY-FRAME:
[00:00] - [Exact position and content of each element]
[00:02] - [Next frame with positions]
...

TEXT BOXES:
- Background: BLACK
- Opacity: 0.8
- Padding: 0.2 units
- Text color: WHITE

COLOR SCHEME:
[Specify colors for each element type]
</scene_plan>
'''

def validate_and_fix_manim_code(code):
    """Perform final validation and fixes on Manim code before saving.
    
    Args:
        code: The generated code to validate
        
    Returns:
        Fixed code or None if unfixable
    """
    if not code:
        return None
        
    # Check for critical errors
    critical_issues = []
    
    # 1. Check for proper import
    if not re.search(r'from\s+manim\s+import\s+\*', code):
        critical_issues.append("Missing 'from manim import *'")
        
    # 2. Check for class definition
    if not re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', code):
        critical_issues.append("Missing Scene class definition")
        
    # 3. Check for construct method
    if not re.search(r'def\s+construct\s*\(\s*self\s*\)', code):
        critical_issues.append("Missing construct method")
    
    if critical_issues:
        print("❌ Critical issues in generated code:")
        for issue in critical_issues:
            print(f"  - {issue}")
        return None
    
    # Apply additional fixes
    
    # 1. Fix any remaining uncommented descriptive text
    lines = code.split('\n')
    fixed_lines = []
    in_class_def = False
    in_function_def = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            fixed_lines.append(line)
            continue
            
        # Track if we're in a class or function definition for proper indentation context
        if re.match(r'\s*class\s+', line):
            in_class_def = True
            in_function_def = False
        elif re.match(r'\s*def\s+', line):
            in_function_def = True
        
        # If already a comment, keep as is
        if stripped.startswith('#'):
            fixed_lines.append(line)
            continue
            
        # Check if this is valid Python
        try:
            compile(line, '<string>', 'single')
            fixed_lines.append(line)  # Valid code, keep as is
        except SyntaxError:
            # Check if this is just descriptive text (no code characters)
            if (in_function_def and not any(char in stripped for char in "={}[](),.+-*/:'\"\\")) or re.match(r'^\s*[A-Z][^={}()\[\]]*$', stripped):
                # Likely a section header or descriptive text, comment it
                leading_space = len(line) - len(line.lstrip())
                fixed_lines.append(' ' * leading_space + '# ' + stripped)
                print(f"⚠️ Line {i+1}: Commented text '{stripped}'")
            else:
                # This is likely code with a syntax error
                fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def enforce_topic_in_code(code, topic):
    """Enforce that the code is about the specified topic by adding relevant content.
    
    Args:
        code: The generated code
        topic: The topic that should be visualized
    
    Returns:
        Modified code with enforced topic references
    """
    topic_lower = topic.lower()
    
    # Topic-specific templates for common math topics
    templates = {
        'eigenvalues': """
        # Define a 2x2 matrix for eigenvalue demonstration
        matrix = [
            [3, 1],
            [1, 2]
        ]
        matrix_mob = Matrix(matrix)
        self.play(Write(matrix_mob))
        self.wait(1)
        
        # Show eigenvalues calculation
        eigenvalues_text = Tex("Eigenvalues: $\\lambda_1 = 4$, $\\lambda_2 = 1$")
        eigenvalues_text.next_to(matrix_mob, DOWN, buff=1)
        self.play(Write(eigenvalues_text))
        self.wait(1)
        """,
        
        'vector': """
        # Create a 2D vector
        vector = Vector([2, 1])
        self.play(Create(vector))
        self.wait(1)
        
        # Label the vector
        vector_label = Tex("\\\\vec{v}")
        vector_label.next_to(vector.get_end(), UP)
        self.play(Write(vector_label))
        self.wait(1)
        """,
        
        'matrix': """
        # Create a matrix
        matrix = [
            [2, 1],
            [1, 3]
        ]
        matrix_mob = Matrix(matrix)
        self.play(Write(matrix_mob))
        self.wait(1)
        
        # Show matrix properties
        determinant = Tex("\\\\det(A) = 5")
        determinant.next_to(matrix_mob, DOWN, buff=1)
        self.play(Write(determinant))
        self.wait(1)
        """,
        
        'calculus': """
        # Show a function
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_tip": False}
        )
        
        # Define and plot f(x) = x^2
        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = MathTex("f(x) = x^2")
        graph_label.next_to(graph.point_from_proportion(0.8), UL)
        
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)
        """
    }
    
    # Find the right template based on the topic
    template_key = None
    for key in templates:
        if key in topic_lower:
            template_key = key
            break
    
    if not template_key:
        # Generic template if no specific match
        template = f"""
        # Create text about {topic}
        explanation = Tex("This animation demonstrates {topic}")
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(1)
        """
    else:
        template = templates[template_key]
    
    # Find position to insert the template (after setup section)
    setup_end = code.find("self.play(title.animate.scale(0.5).to_edge(UP))")
    if setup_end != -1:
        next_line_pos = code.find("\n", setup_end) + 1
        modified_code = code[:next_line_pos] + "\n        self.wait(1)\n" + template + code[next_line_pos:]
        return modified_code
    
    return code