# More detailed prompts for handling complex exercise visualization
EXERCISE_EXTRACTION = '''You are an AI assistant specialized in breaking down mathematical exercises for visualization. Your task is to extract the key concept that needs to be visualized from a complex problem.

<exercise>
{topic}
</exercise>

<macro_topic>
{macro_topic}
</macro_topic>

First, analyze the exercise:

<exercise_analysis>
1. Core Concept: [What is the main mathematical idea being tested]
2. Solution Steps: [Break down the solution process]
3. Key Visualization Needs: [What aspects would benefit most from visualization]
4. Student Understanding: [What do students need to grasp to solve this]
</exercise_analysis>

<visualization_focus>
Based on your analysis, identify ONE key concept or step that would most benefit from visualization.
This should be something that can be clearly shown in a 15-second animation.
</visualization_focus>
'''

EXERCISE_DESIGN = '''Design a 15-second animation that helps understand this mathematical exercise.

<exercise>
{topic}
</exercise>

<visualization_focus>
{visualization_focus}
</visualization_focus>

Your animation must:
1. Focus on the key concept identified
2. Show a specific example that illustrates the concept
3. Highlight the problem-solving process
4. Keep text and equations clear of the main animation
5. Use color coding to show relationships
6. Include proper spacing and timing for comprehension

<animation_design>
[Provide a detailed, frame-by-frame description of the animation]
</animation_design>
''' 