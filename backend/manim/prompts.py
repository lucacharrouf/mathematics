import re

# =============================================================================
# Core Prompts for Manim Animation Generation
# =============================================================================

CONCEPT_BREAKDOWN = '''You are an AI assistant specializing in breaking down mathematical concepts for visualization. Before designing an animation, you need to analyze the concept and identify the best approach to visualize it.

<math_topic>
{topic}
</math_topic>

<audience>
{audience_level}
</audience>

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
</concept_analysis>

<visualization_approach>
Based on the analysis above, recommend the most effective approach for visualizing this concept in a 15-second animation. Explain why this approach would be most effective for building understanding.
</visualization_approach>

<key_visual_elements>
List the specific visual elements that should be included in the animation to effectively convey this concept:
1. [Element 1 with justification]
2. [Element 2 with justification]
3. [Element 3 with justification]
...
</key_visual_elements>
'''

# Animation design prompt - creating a description for the animation
DESIGN = '''You are an AI assistant specialized in creating educational mathematical animations. Your task is to design a 15-second animation explaining a mathematical concept.

Part 1: Animation Design

Here is the mathematical topic you need to cover in your animation:

<math_topic>
{topic}
</math_topic>

<audience>
{audience_level}
</audience>

Your goal is to create a visually engaging and informative scene that explains this concept. Follow these steps:

1. Analyze the given mathematical topic and identify key concepts for visualization.
2. Plan visual elements and transitions to explain these concepts.
3. Describe the scene in detail, including mathematical objects, movements, text, equations, and timing.
4. Explain how each visual element relates to the mathematical concept.
5. Ensure your description is clear enough for code generation.

Before providing your final animation description, wrap your animation planning process inside <animation_timeline> tags in your thinking block. Create a timeline of the 15-second animation, breaking it down into 3-second segments and describing what happens in each. Consider:
- Key mathematical concepts related to the topic
- Potential visual representations for each concept
- Color schemes and transitions to enhance understanding
- Breaking down the concept into visually representable parts
- Analogies or real-world examples to illustrate the concept
- Use of color, movement, or transitions to enhance understanding
- How to make abstract concepts tangible and intuitive
- Progressive disclosure of information to avoid overwhelming the viewer

It's OK for this section to be quite long.

<pedagogy_principles>
Follow these educational design principles:
1. Start with concrete examples before abstract concepts
2. Use visual metaphors that connect to everyday experiences
3. Highlight cause-and-effect relationships
4. Show both the "what" and the "why" of the concept
5. Include at least one intuitive explanation alongside formal definitions
6. Use consistent visual language (colors, shapes) to represent related concepts
7. Break complex ideas into sequential, buildable steps
8. When possible, show a practical application of the concept
</pedagogy_principles>

After your planning, provide your animation description in this format:

<animation_design>
<scene_description>
[Detailed description of the 15-second animation, including all visual elements and their timing]
</scene_description>

<mathematical_explanation>
[Explanation of how the visual elements relate to the mathematical concept]
</mathematical_explanation>

<key_points>
[List of the main mathematical ideas conveyed in the animation]
</key_points>

<intuition_building>
[Describe specific ways the animation builds intuition about the concept rather than just showing it]
</intuition_building>
</animation_design>

<self_evaluation>
[Evaluate the strengths and potential weaknesses of your design. Consider:
- Clarity of explanation
- Visual appeal
- Educational value
- Feasibility of implementation in MANIM
- Whether it would help someone truly understand the concept, not just see it
- If the animation would still make sense with the sound off
Suggest any improvements if necessary.]
</self_evaluation>

Your final output for Part 1 should consist only of the <animation_design> and <self_evaluation> sections, and should not duplicate or rehash any of the work you did in the thinking block.'''

# Animation testing prompt - evaluating the animation design
ANIMATION_TESTING = '''You are an AI assistant specializing in evaluating mathematical animations. You'll review a proposed animation design and identify potential issues before implementation.

<math_topic>
{topic}
</math_topic>

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

CODE_GENERATION = '''You are an expert in creating mathematical animations using the Manim Python library. Your task is to generate code for an animation about the following topic:

<topic>
{{TOPIC}}
</topic>

The class name for this animation should be:

<class_name>
{{SAFE_CLASS_NAME}}
</class_name>

Here is the design specification for the animation:

<design_specification>
{{design_scene}}
</design_specification>

Before writing the code, please plan out the animation in detail. Wrap your planning process in <animation_planning> tags. In your planning:

[Planning steps remain the same...]

After planning, generate the Manim code for the animation. Your code must adhere to the following requirements:

[Requirements remain the same...]

After writing the code, perform a self-evaluation. Consider the following:

[Evaluation points remain the same...]

ABSOLUTELY CRITICAL FORMATTING INSTRUCTIONS:
- You MUST use the EXACT tags specified below
- DO NOT use markdown formatting or triple backticks for the code section
- The tags must appear EXACTLY as shown, with no additional characters or spaces

Present your response in the following format:

<animation_planning>
[Your detailed planning for the animation]
</animation_planning>

<CODE_START>
[Your complete Python code for the Manim animation]
<CODE_END>

<code_self_evaluation>
[Your evaluation of the code, addressing the points mentioned above]
</code_self_evaluation>

IMPORTANT: The code section MUST start with <CODE_START> and end with <CODE_END> exactly as shown - do not use triple backticks or any markdown formatting. This is critical for the automated system to process your response correctly.'''
# =============================================================================
# Helper Functions
# =============================================================================

def extract_code_only(text, topic=None):
    """Extract code from between <CODE_START> and <CODE_END> tags with topic validation.
    
    Args:
        text: The response text from the API
        topic: Optional topic for validation
        
    Returns:
        The extracted code if valid, or None if extraction failed or validation failed
    """
    if not text:
        print("Error: Empty response received")
        return None
        
    # Try standard pattern first - this is the primary method that should be used
    pattern = r'<CODE_START>(.*?)<CODE_END>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        # If topic is provided, validate the code is about the topic
        if topic and not validate_topic_relevance(code, topic):
            print(f"Warning: Extracted code does not appear to be about '{topic}'")
            return None
        return code
    
    # If standard pattern doesn't match, we have a formatting problem
    print("Warning: <CODE_START> and <CODE_END> tags not found in response")
    
    # If topic validation is required, don't use fallback methods for safety
    if topic:
        print("ERROR: Strict topic validation required but <CODE_START> tags not found")
        print("Skipping fallback extraction methods for topic safety")
        return None
    
    # Only use fallback methods when topic validation is not required
    # Look for code blocks in markdown format
    pattern = r'```python\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try any code block
    pattern = r'```\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        if "import" in code or "class" in code:
            return code
    
    # Last resort fallbacks - these should rarely be needed with improved prompts
    if "from manim import" in text:
        start_idx = text.find("from manim import")
        end_markers = ["\n\n<code_self_evaluation>", "\n\n---", "\n\nThis code"]
        end_idx = len(text)
        for marker in end_markers:
            marker_pos = text.find(marker, start_idx)
            if marker_pos != -1 and marker_pos < end_idx:
                end_idx = marker_pos
        return text[start_idx:end_idx].strip()
    
    # Look for a class definition with Scene
    pattern = r'class\s+\w+\s*\(\s*Scene\s*\).*?def\s+construct\s*\(\s*self\s*\)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        start_idx = match.start()
        import_idx = text.rfind("import", 0, start_idx)
        if import_idx != -1:
            line_start = text.rfind("\n", 0, import_idx)
            if line_start != -1:
                start_idx = line_start + 1
            else:
                start_idx = 0
        end_idx = len(text)
        end_markers = ["\n\n<code_self_evaluation>", "\n\n---", "\n\nThis code"]
        for marker in end_markers:
            marker_pos = text.find(marker, start_idx)
            if marker_pos != -1:
                end_idx = marker_pos
                break
        return text[start_idx:end_idx].strip()
    
    print("Warning: Could not extract code using any method")
    return None

def validate_topic_relevance(code, topic):
    """Check if code is relevant to the requested topic with stricter validation.
    
    Args:
        code: The extracted code
        topic: The topic to validate against
        
    Returns:
        True if the code is relevant to the topic, False otherwise
    """
    if not code or not topic:
        return False
    
    # Get meaningful keywords from the topic
    topic_keywords = [word.lower() for word in topic.lower().split() if len(word) > 3]
    if not topic_keywords:
        topic_keywords = [topic.lower()]
    
    # Add full phrase for multi-word topics
    full_topic = topic.lower()
    if ' ' in full_topic:
        topic_keywords.append(full_topic)
    
    # Extract the class name from the code
    class_match = re.search(r'class\s+(\w+)', code)
    class_name = class_match.group(1).lower() if class_match else ""
    
    # Extract all comments from the code
    comment_lines = [line.split('#')[1].strip() if '#' in line and line.strip()[0] != '#' else "" 
                    for line in code.split('\n') if '#' in line]
    comments_text = ' '.join(comment_lines).lower()
    
    # Extract string literals from the code
    string_literals = re.findall(r'"([^"]*)"', code) + re.findall(r"'([^']*)'", code)
    strings_text = ' '.join(string_literals).lower()
    
    # Check for full topic phrase in class name, comments or strings (highest priority)
    if full_topic in class_name or full_topic in comments_text or full_topic in strings_text:
        return True
    
    # For multi-word topics, require at least 2 keywords to match or a minimum percentage
    if len(topic_keywords) > 1:
        # Count matches across all sources
        matches = sum(1 for keyword in topic_keywords if 
                     keyword in class_name or 
                     keyword in comments_text or 
                     keyword in strings_text)
        
        # Require either at least 2 keywords to match or 60% of all keywords
        min_matches = max(2, int(len(topic_keywords) * 0.6))
        
        if matches < min_matches:
            print(f"Warning: Only {matches}/{len(topic_keywords)} keywords from '{topic}' found in code")
            print(f"Keywords present: {[kw for kw in topic_keywords if kw in class_name or kw in comments_text or kw in strings_text]}")
            
            # Check for unrelated topics explicitly mentioned
            docstring_match = re.search(r'"""(.*?)"""', code, re.DOTALL)
            if docstring_match:
                docstring = docstring_match.group(1).lower()
                # If docstring mentions a different animation topic clearly
                if any(phrase in docstring for phrase in ["animation for", "animation of", "visualizing", "visualization of"]):
                    actual_topic = None
                    for line in docstring.split('\n'):
                        if any(phrase in line for phrase in ["animation for", "animation of", "visualizing", "visualization of"]):
                            # Try to extract the actual topic
                            words_after = re.search(r'(?:animation for|animation of|visualizing|visualization of)\s+(.+)', line)
                            if words_after:
                                actual_topic = words_after.group(1).strip()
                                break
                    
                    if actual_topic and full_topic not in actual_topic:
                        print(f"ERROR: Code appears to be about '{actual_topic}' instead of '{topic}'")
                        return False
            
            return False
    else:
        # For single-word topics, we need strong evidence
        # The keyword should appear multiple times or in a prominent place like the class name
        keyword = topic_keywords[0]
        count_in_code = (class_name.count(keyword) * 3 +  # Class name matches count triple
                         comments_text.count(keyword) + 
                         strings_text.count(keyword))
        
        if count_in_code < 2:
            print(f"Warning: Topic '{topic}' is not prominent in the code (only {count_in_code} occurrences)")
            return False
    
    # Check for unrelated topics (known problematic topics)
    problem_topics = ["kinematic equation", "binary search", "binary tree", "angle between vectors",
                      "angle in 3d", "vector cross product", "vector dot product"]
    
    for problem in problem_topics:
        # Skip if the problem topic contains the requested topic
        if full_topic in problem:
            continue
            
        # Check if code is explicitly about a different topic
        prominent_mentions = (
            problem in class_name or
            comments_text.count(problem) > 1 or
            strings_text.count(problem) > 1
        )
        
        if prominent_mentions:
            print(f"ERROR: Code appears to be about '{problem}' instead of '{topic}'")
            return False
    
    return True

def extract_section(text, section_name):
    """Extract content from a specific XML-like section
    
    Args:
        text: The text to extract from
        section_name: The name of the section to extract
        
    Returns:
        The extracted section content, or None if not found
    """
    if not text or not section_name:
        return None
        
    pattern = rf'<{section_name}>(.*?)</{section_name}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
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

def format_code_generation_prompt(topic, design_scene):
    """Format the code generation prompt with topic-specific information
    
    Args:
        topic: The mathematical topic
        design_scene: The design specification
        
    Returns:
        Formatted prompt string
    """
    safe_class_name = create_topic_safe_classname(topic)
    
    # Replace placeholders in the prompt
    formatted_prompt = CODE_GENERATION.format(
        topic=topic,
        design_scene=design_scene,
        safe_class_name=safe_class_name
    )
    
    return formatted_prompt