# Add this at the top of the file with other imports
import re

# 1. Video Orchestrator Prompts
VIDEO_IDEA_GENERATOR_SYSTEM_PROMPT = """You are an expert designing videos that are created using the python library for Manim.
The videos will explain topics that may be complicated, so the video must walk them through step by step so that they can go from not knowing much to feeling really confident about the topic.

STRUCTURE YOUR VIDEO PLAN WITH:
1. Pre-Requisites Scene (15-20 seconds): Introduce foundational concepts needed to understand the main topic
2. Core Concept Scenes (3-4 scenes, 20-30 seconds each): Systematically explain main concepts
3. Application Scene (15-20 seconds): Show how the concept is used in practice

SCENE GUIDELINES:
- Each scene must be completely independent (don't mention other scenes)
- Each scene should focus on ONE key idea or step in the explanation
- Use concrete examples with specific numbers, vectors, or matrices
- Build complexity gradually - start simple, then add depth
- Include visualizations that highlight the mathematical relationships
- Limit each scene to 3-4 visual elements at any time

TIMING:
- Total video duration: 1.5-2.5 minutes 
- Each scene: 15-30 seconds

AVOID:
- Complex real-world objects (difficult to implement in Manim)
- Overly crowded screens with too many elements
- Abstract explanations without visual reinforcement
"""

VIDEO_IDEA_GENERATOR_USER_PROMPT = """The video topic is:

{video_prompt}

Generate 4-6 detailed scene ideas that progressively teach this concept. For each scene, include:
1. The specific mathematical content to be visualized
2. Key equations or formulas to include (if applicable)
3. Visual elements that would effectively demonstrate the concept
4. How this scene contributes to overall understanding"""

# 2. Scene Planner Prompts
SCENE_PLANNER_SYSTEM_PROMPT = """You are an expert manim scene planner with strong visual taste and deep understanding of mathematical visualization.

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

5. Mathematical Rigor:
   - Use mathematically correct examples
   - Show appropriate notation and labels
   - Ensure formulas and equations are correctly typeset
   - Demonstrate the concept with specific numeric examples
"""

SCENE_PLAN_USER_PROMPT = """This is the scene to implement:

{scene_prompt}

Create a detailed scene plan with:

1. FRAME-BY-FRAME BREAKDOWN:
   - [00:00] Introduction - What text and objects appear
   - [00:05] First concept - Describe exact visuals
   - [00:10] Second concept - Detail any transformations
   - [00:15] Conclusion - Final elements shown

2. POSITIONING DETAILS:
   - Specify exact coordinates for key elements
   - Describe text placements (top, bottom, next to objects)
   - Plan for smooth transitions between elements

3. MATHEMATICAL CONTENT:
   - Specify exact equations to be shown
   - Provide concrete values for vectors, matrices, or functions
   - List labels for all mathematical objects

The scene should be 20-30 seconds long and thoroughly explain a single concept."""

SCENE_EVALUATOR_SYSTEM_PROMPT = """Evaluate the plan for the Manim animation against these CRITICAL criteria:

1. Mathematical Correctness:
   - Are all equations and formulas mathematically accurate?
   - Are all values and calculations correct?
   - Are the examples appropriate for demonstrating the concept?

2. Visual Clarity:
   - Is text properly separated from visual elements?
   - Is the screen properly zoned (TOP for titles, MIDDLE for visuals, BOTTOM for explanations)?
   - Are objects properly spaced to avoid overlap?
   - Are no more than 3-4 elements visible at once?

3. Narrative Flow:
   - Does the scene build concepts progressively?
   - Are elements introduced one at a time with proper pauses?
   - Is there clear connection between text explanations and visual elements?

4. Technical Feasibility:
   - Are all animations implementable in Manim?
   - Are complex transitions broken down into manageable steps?
   - Are coordinates and positions clearly specified?

The plan must ensure that text is not overlapping other objects and all items fit properly on screen.
"""

SCENE_EVALUATION_USER_PROMPT = """Evaluate this scene plan and identify any issues that need correction:

Scene Plan:
{scene_plan}

Provide specific feedback on:
1. Mathematical accuracy and rigor
2. Screen layout and object positioning 
3. Pacing and timing
4. Element visibility and clarity

If the plan does not meet any criteria, explain exactly what needs to be fixed."""

# 3. Code Generator Prompts
CODE_GENERATOR_SYSTEM_PROMPT = """You are an expert in the Manim python library for creating mathematical animations.

CRITICAL CODING REQUIREMENTS:

1. IMPORTS AND STRUCTURE:
   - ALWAYS begin with: from manim import *
   - Put ALL logic in the construct() method
   - Follow the Scene class structure precisely

2. SCREEN BOUNDARIES AND POSITIONING:
   - The visible frame is from x=-7 to x=7 and y=-4 to y=4
   - ALWAYS position elements with these boundaries in mind
   - Use these positioning techniques:
     • title.to_edge(UP, buff=0.5)  # Safely position at top
     • text.to_edge(DOWN, buff=0.5)  # Safely position at bottom
     • element.move_to(ORIGIN)  # Center on screen
     • element.next_to(other_element, direction, buff=0.5)  # Position relative to other elements
   - For long text: text.scale(0.8) or break into multiple lines
   - Add frame_width parameter for wider objects: self.camera.frame_width = 14

3. TEXT AND MATHEMATICAL OBJECTS:
   - Always set font_size for Text objects: Text("text", font_size=30)
   - For long explanations, break into multiple lines or text objects
   - For improved visibility, use background rectangles:
     ```python
     explanation = Text("Important explanation", font_size=24)
     explanation.to_edge(DOWN, buff=0.5)
     explanation_bg = SurroundingRectangle(explanation, color=WHITE, fill_opacity=0.1)
     self.play(FadeIn(explanation_bg), Write(explanation))
     ```

4. ANIMATION TECHNIQUES:
   - Introduce elements one at a time
   - Wait after each new element (self.wait(1))
   - Clear screen before introducing new concepts: self.play(FadeOut(*self.mobjects))

5. EXAMPLE OF BOUNDARY-SAFE CODE:
```python
def construct(self):
    # Title in TOP zone with safe positioning
    title = Text("Vector Addition", font_size=40)
    title.to_edge(UP, buff=0.5)
    
    # Check if title is too wide and scale down if needed
    if title.width > 12:
        title.scale(12/title.width)
    
    self.play(Write(title))
    self.wait(1)
    
    # Main content in MIDDLE zone
    vector1 = Vector([2, 1], color=BLUE)
    vector1.move_to(ORIGIN)  # Center positioning
    
    # Safe text positioning with background
    explanation = Text("This is a vector", font_size=30)
    explanation.to_edge(DOWN, buff=0.5)
    explanation_bg = SurroundingRectangle(
        explanation, 
        fill_color=BLACK,
        fill_opacity=0.8,
        buff=0.2,
        color=WHITE
    )
    
    self.play(Create(vector1))
    self.play(FadeIn(explanation_bg), Write(explanation))
    self.wait(2)
    
    # Clear screen safely
    self.play(FadeOut(*self.mobjects))
    self.wait(0.5)
```

IMPORTANT LAYOUT GUIDELINES:
1. Ensure all text and animations stay within the standard Manim frame (-7.1 to 7.1 horizontally, -4 to 4 vertically)
2. Add padding of at least 0.5 units from all frame edges
3. Never place text on top of other text or complex animations
4. For sequential animations, clear previous elements or move them to non-interfering positions
5. When showing multiple elements simultaneously, position them with clear spacing (at least 1 unit apart)
6. Use UP, DOWN, LEFT, RIGHT constants with appropriate values for positioning
7. Always add background rectangles with slight opacity behind text for better readability
8. Divide the screen into logical zones and maintain separation between zones

"""

CODE_GENERATOR_USER_PROMPT = """Generate the manim code for this scene plan:

{code_spec}

The code MUST:
1. Include correct "from manim import *" import
2. Follow the Scene class structure
3. Position all elements according to proper screen zones
4. Include all mathematical content specified in the plan
5. Use appropriate animations with proper timing and waits
6. Ensure text and objects don't overlap
7. Include all the details from the scene plan

Format your response with ```python tags around the code."""

# Enhanced validation and utility functions
def extract_code_with_retries(response, max_attempts=3):
    """Extract code between ```python tags with retries."""
    for attempt in range(max_attempts):
        code = extract_code_from_response(response)
        if code:
            return code
            
        # If we're here, code extraction failed
        print(f"Attempt {attempt+1} failed to extract code")
        
    return None

def validate_and_fix_manim_code(code):
    """Perform enhanced validation and fixes on Manim code."""
    if not code:
        return None
        
    # Check for critical errors
    critical_issues = []
    
    # 1. Check for proper import
    if not re.search(r'from\s+manim\s+import\s+\*', code):
        print("⚠️ Fixing missing or incomplete import statement")
        code = re.sub(r'^from\s+manim\s+import\s*(\w+,?\s*)*$', 'from manim import *', code, flags=re.MULTILINE)
        if not re.search(r'from\s+manim\s+import', code):
            code = "from manim import *\n\n" + code
    
    # 2. Check for class definition
    if not re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', code):
        critical_issues.append("Missing Scene class definition")
    
    # 3. Check for construct method
    if not re.search(r'def\s+construct\s*\(\s*self\s*\)', code):
        critical_issues.append("Missing construct method")
    
    if len(critical_issues) > 0:
        print("❌ Critical issues in generated code:")
        for issue in critical_issues:
            print(f"  - {issue}")
        if len(critical_issues) > 1:
            return None
    
    # Fix uncommented descriptive text
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

# 4. Code Layout Evaluation Prompts
CODE_LAYOUT_EVALUATOR_SYSTEM_PROMPT = """You are an expert in reviewing Manim animation code to ensure perfect visual layout.
Focus EXCLUSIVELY on identifying and fixing these critical layout issues:

1. SCREEN BOUNDARY ENFORCEMENT:
   - CRITICAL: All text and objects MUST stay within screen boundaries
   - The standard frame is from x=-7 to x=7 and y=-4 to y=4
   - Text must be at least 0.5 units away from screen edges
   - Long text should be scaled down or broken into multiple lines
   - For critical boundary fixes, use to_edge() with appropriate buff values

2. ELEMENT OVERLAP:
   - Check if text elements might overlap with other visual elements
   - Verify that animations don't cause objects to cross paths inappropriately
   - Ensure objects have adequate spacing (minimum 0.5 units between elements)

3. SCREEN ZONE DISCIPLINE:
   - Title text MUST be in TOP ZONE (y > 2, but no higher than y=3.5)
   - Main visuals MUST be in MIDDLE ZONE (-2 < y < 2)
   - Explanatory text MUST be in BOTTOM ZONE (y < -2, but no lower than y=-3.5)

4. TEXT SIZING AND READABILITY:
   - Set appropriate font_size for all Text() and MathTex() objects
   - Scale down text that's too wide (width > 10)
   - Add background rectangles behind text for better visibility
   - For long explanations, use multiple shorter text objects

5. VISUALIZATION:
   - Elements should have sufficient scale to be clearly visible
   - Critical elements should be positioned centrally
   - Use appropriate colors with good contrast

DO NOT comment on the mathematical content or code structure.
Focus ONLY on layout, positioning, and boundary enforcement.
"""

CODE_LAYOUT_EVALUATION_USER_PROMPT = """Review this Manim code for layout issues:

```python
{code}
```

Identify ONLY issues related to:
1. Elements that might overlap
2. Improper use of screen zones
3. Visual clutter or too many elements
4. Positioning problems

For each issue, provide:
1. The specific line numbers where the problem occurs
2. A clear explanation of the issue
3. The EXACT code fix needed

If you find any critical layout problems, provide a COMPLETE fixed version of the problematic section.
"""

def evaluate_and_fix_layout(code, get_llm_response_func=None):
    """Submit code for layout evaluation and implement suggested fixes.
    
    Args:
        code: The generated Manim code
        get_llm_response_func: Function to get LLM response
        
    Returns:
        Fixed code with improved layout
    """
    if not code:
        return None
        
    if get_llm_response_func is None:
        print("⚠️ No LLM response function provided, skipping layout evaluation")
        return code
        
    try:
        # Combine the prompts
        layout_evaluation_prompt = CODE_LAYOUT_EVALUATOR_SYSTEM_PROMPT + "\n\n" + CODE_LAYOUT_EVALUATION_USER_PROMPT.format(code=code)
        
        # Send to LLM for evaluation
        print("Evaluating code layout and spacing...")
        evaluation_response = get_llm_response_func(
            system_prompt=CODE_LAYOUT_EVALUATOR_SYSTEM_PROMPT,
            user_prompt=CODE_LAYOUT_EVALUATION_USER_PROMPT.format(code=code)
        )
        
        # Look for fixed code sections in the response
        fixed_code_blocks = re.findall(r'```python\s*(.*?)\s*```', evaluation_response, re.DOTALL)
        
        # If there's a complete fixed code block, use it
        if fixed_code_blocks and len(fixed_code_blocks[-1]) > len(code)/2:
            fixed_code = fixed_code_blocks[-1]
            print("✓ Applied comprehensive layout fixes")
            return fixed_code
            
        # Look for specific line fixes
        line_fixes = re.findall(r'Line (\d+).*?:\s*(.*?)(?=\n\n|\nLine|\Z)', evaluation_response, re.DOTALL)
        
        if line_fixes:
            # Apply individual line fixes
            lines = code.split('\n')
            for line_num_str, fix_comment in line_fixes:
                try:
                    line_num = int(line_num_str) - 1  # Convert to 0-based index
                    if 0 <= line_num < len(lines):
                        # Extract code snippet from fix comment
                        code_snippet_match = re.search(r'```python\s*(.*?)\s*```', fix_comment, re.DOTALL)
                        if code_snippet_match:
                            replacement = code_snippet_match.group(1).strip()
                            # Replace the problematic line
                            lines[line_num] = replacement
                            print(f"✓ Applied fix to line {line_num+1}")
                except ValueError:
                    print(f"⚠️ Could not parse line number: {line_num_str}")
                    
            fixed_code = '\n'.join(lines)
            print("✓ Applied targeted layout fixes")
            return fixed_code
            
        # Check if there are no issues
        if "No layout issues found" in evaluation_response or "no issues" in evaluation_response.lower():
            print("✓ Code layout evaluation passed - no issues found")
            return code
            
        # If we can't find specific fixes but there are issues
        print("⚠️ Layout issues identified but no specific fixes provided")
        return code
            
    except Exception as e:
        print(f"⚠️ Error during layout evaluation: {str(e)}")
        return code 

def enforce_boundary_checks(code):
    """Add comprehensive boundary checks to ensure all elements stay within screen boundaries."""
    # 1. First, add the safe_position utility function to the Scene class
    class_match = re.search(r'class\s+(\w+)\s*\(Scene\):\s*\n', code)
    if class_match:
        class_name = class_match.group(1)
        utility_function = """
    def safe_position(self, mobject, zone="MIDDLE", buff=0.5):
        \"\"\"Ensure mobject stays within screen boundaries.\"\"\"
        # Get frame boundaries (adjust if camera.frame_width was changed)
        frame_width = getattr(self.camera, "frame_width", 14)
        frame_height = getattr(self.camera, "frame_height", 8)
        max_x = frame_width/2 - buff
        max_y = frame_height/2 - buff
        
        # Set position based on zone
        if zone == "TOP":
            mobject.to_edge(UP, buff=buff)
            # Limit y position
            if mobject.get_top()[1] > max_y:
                mobject.shift(DOWN * (mobject.get_top()[1] - max_y))
        elif zone == "BOTTOM":
            mobject.to_edge(DOWN, buff=buff)
            # Limit y position
            if mobject.get_bottom()[1] < -max_y:
                mobject.shift(UP * (-max_y - mobject.get_bottom()[1]))
        else:  # MIDDLE zone or anything else
            # Only adjust if outside boundaries
            if mobject.get_center()[1] > max_y - mobject.height/2:
                mobject.align_to(UP * (max_y - mobject.height/2), UP)
            if mobject.get_center()[1] < -max_y + mobject.height/2:
                mobject.align_to(DOWN * (max_y - mobject.height/2), DOWN)
        
        # Check width and scale down if needed
        if mobject.width > frame_width - 2*buff:
            scale_factor = (frame_width - 2*buff) / mobject.width
            mobject.scale(scale_factor)
        
        # Check horizontal boundaries
        if mobject.get_right()[0] > max_x:
            mobject.shift(LEFT * (mobject.get_right()[0] - max_x))
        if mobject.get_left()[0] < -max_x:
            mobject.shift(RIGHT * (-max_x - mobject.get_left()[0]))
        
        return mobject
"""
        
        # Insert after class definition
        code = re.sub(
            r'(class\s+\w+\s*\(Scene\):\s*\n)(\s*def\s+construct)',
            r'\1' + utility_function + r'\2',
            code
        )
    
    # 2. Add camera frame setting to ensure consistent boundaries
    construct_match = re.search(r'(\s*def\s+construct\s*\(\s*self\s*\):)', code)
    if construct_match:
        frame_settings = """
        # Set frame dimensions for consistent boundaries
        self.camera.frame_width = 14
        self.camera.frame_height = 8
"""
        code = code.replace(
            construct_match.group(0),
            construct_match.group(0) + frame_settings
        )
    
    # 3. Fix coordinate dimensions for Dot creation
    # Look for 2D coordinates and convert them to 3D
    coord_pattern = r'(\w+_coords\s*=\s*\[(?:\s*\([^)]+\)\s*,?)+\])'
    for match in re.finditer(coord_pattern, code):
        coords_def = match.group(1)
        # Check if we have 2D coordinates (no third component)
        if re.search(r'\(\s*-?\d+\.?\d*\s*,\s*-?\d+\.?\d*\s*\)', coords_def):
            # Replace with 3D coordinates by adding ,0 as the z-coordinate
            fixed_coords = re.sub(
                r'\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)',
                r'(\1, \2, 0)',
                coords_def
            )
            code = code.replace(coords_def, fixed_coords)
    
    # 4. Alternative approach: Fix Dot creation instead of coordinates
    dot_pattern = r'Dot\(\s*([^,)]+)(?:\s*,|\s*\))'
    for match in re.finditer(dot_pattern, code):
        point_var = match.group(1).strip()
        # Only fix if it's using a direct variable (not a complex expression)
        if re.match(r'^[a-zA-Z_]\w*$', point_var) and "point" not in point_var:
            # Add np.array with 3rd component if it's a plain variable
            replacement = f"Dot(np.array([{point_var}[0], {point_var}[1], 0])"
            code = code.replace(f"Dot({point_var}", replacement)
    
    # 5. Add numpy import if needed
    if "np.array" in code and "import numpy" not in code:
        code = re.sub(
            r'from manim import \*',
            'from manim import *\nimport numpy as np',
            code
        )
    
    # 6. Add safety checks at the end as before
    # Find all text objects
    text_objects = re.findall(r'(\w+)\s*=\s*(Text|MathTex|Tex)\(', code)
    
    # Find the last line of the construct method to append our safe positioning code
    construct_end = code.rfind('def construct')
    if construct_end != -1:
        # Find where to insert our safe positioning code
        # Look for the last self.play or self.wait call
        last_play = max(code.rfind('self.play('), code.rfind('self.wait('))
        if last_play != -1:
            # Find the end of this line
            line_end = code.find('\n', last_play)
            if line_end != -1:
                # Insert our safe positioning code
                safety_code = "\n        # Ensure all text elements stay within screen boundaries\n"
                for var_name, obj_type in text_objects:
                    zone = "TOP" if "title" in var_name.lower() else "BOTTOM" if any(x in var_name.lower() for x in ["explain", "description", "summary"]) else "MIDDLE"
                    safety_code += f"        # Safe position for {var_name}\n"
                    safety_code += f"        if '{var_name}' in locals():\n"
                    safety_code += f"            self.safe_position({var_name}, zone=\"{zone}\", buff=0.5)\n"
                    
                # Add background rectangles
                for var_name, obj_type in text_objects:
                    safety_code += f"""
        # Add background for better visibility for {var_name}
        if '{var_name}' in locals() and '{var_name}_bg' not in locals():
            {var_name}_bg = SurroundingRectangle({var_name}, fill_opacity=0.85, fill_color=BLACK, buff=0.15)
            {var_name}_group = VGroup({var_name}_bg, {var_name})
"""
                
                # Insert the safety code
                code = code[:line_end+1] + safety_code + code[line_end+1:]
    
    # 7. Check for problematic regex group references that might cause syntax errors
    if re.search(r'\\[0-9]', code):
        code = re.sub(r'\\[0-9]', '', code)
    
    # Additional fix for commented out z-coordinates in move_to calls
    code = re.sub(
        r'move_to\(\s*\[\s*([^,\]]+),\s*([^,\]]+),?\s*(?:#\s*0)?\s*\]\s*\)',
        r'move_to([\1, \2, 0])',
        code
    )
    
    # Fix for missing z-coordinate in any coordinate arrays
    code = re.sub(
        r'(\w+\.move_to\(\[)([^,\]]+),\s*([^,\]]+)(\s*\]\))',
        r'\1\2, \3, 0\4',
        code
    )
    
    return code 

# Add this new prompt to the file

KEY_TAKEAWAYS_SYSTEM_PROMPT = """You are an expert mathematics educator. Your task is to provide clear, concise 
takeaways about mathematical concepts. Focus only on the most fundamental ideas that are essential for understanding.
"""

KEY_TAKEAWAYS_USER_PROMPT = """For the mathematical topic: "{topic}"

Provide the 3-5 most important takeaways that someone must understand about this concept. 
Your response should be 50-60 words total, extremely concise, and focus only on the core mathematical principles.

Format each takeaway as a bullet point starting with •
"""

def generate_key_takeaways(topic, get_llm_response_func):
    """Generate a concise summary of key takeaways for a mathematical topic.
    
    Args:
        topic: Mathematical topic to summarize
        get_llm_response_func: Function to get LLM response
        
    Returns:
        String containing the key takeaways (50-60 words)
    """
    try:
        # Get the key takeaways from the LLM
        response = get_llm_response_func(
            system_prompt=KEY_TAKEAWAYS_SYSTEM_PROMPT,
            user_prompt=KEY_TAKEAWAYS_USER_PROMPT.format(topic=topic)
        )
        
        # Clean up the response
        takeaways = response.strip()
        
        # Verify we got something reasonable (basic validation)
        if len(takeaways.split()) < 10 or "•" not in takeaways:
            # Try one more time with more explicit instructions
            response = get_llm_response_func(
                system_prompt=KEY_TAKEAWAYS_SYSTEM_PROMPT,
                user_prompt=f"""The mathematical topic is: "{topic}"

Please provide EXACTLY 3 bullet points (starting with •) that summarize the most essential concepts.
Each bullet point should be 15-20 words. Focus only on core mathematical principles.
Total length should be 50-60 words maximum."""
            )
            takeaways = response.strip()
        
        return takeaways
        
    except Exception as e:
        print(f"⚠️ Error generating key takeaways: {str(e)}")
        return f"• {topic} is an important mathematical concept.\n• Understanding its foundations helps build mathematical intuition.\n• It has applications in various areas of mathematics and science." 