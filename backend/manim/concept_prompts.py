# Simpler, more direct prompts for concept visualization
CONCEPT_EXTRACTION = '''You are an AI assistant specialized in visualizing mathematical concepts. Your task is to create a clear, focused visualization of a mathematical concept.

<topic>
{topic}
</topic>

<macro_topic>
{macro_topic}
</macro_topic>

IMPORTANT: You must wrap your response in the appropriate XML tags as shown below.

<concept_analysis>
1. Core Definition: [What is the fundamental definition]
2. Visual Components: [What visual elements best represent this concept]
3. Key Properties: [What properties should be highlighted]
4. Common Misconceptions: [What aspects are often misunderstood]
</concept_analysis>

<visualization_focus>
[Your clear, focused statement of what should be visualized. Focus on one main idea that can be clearly shown in a 15-second animation.]
</visualization_focus>

CRITICAL: Your response MUST include both the <concept_analysis> and <visualization_focus> sections with the exact tags shown above.
'''

CONCEPT_DESIGN = '''Design a 15-second animation that clearly explains this mathematical concept.

<topic>
{topic}
</topic>

<visualization_focus>
{visualization_focus}
</visualization_focus>

Your animation must:
1. Start with a clear, simple introduction
2. Build the concept step by step
3. Use consistent color coding and visual language
4. Keep text separate from the main animation area
5. Use proper spacing and timing for readability

CRITICAL: You MUST wrap your animation design in XML tags exactly as shown below:

<animation_design>
Frame 0-2s:
[Describe what happens]

Frame 2-4s:
[Describe what happens]

[Continue frame by frame description...]
</animation_design>

DO NOT use markdown formatting or headers. Use ONLY the XML tags shown above.
''' 