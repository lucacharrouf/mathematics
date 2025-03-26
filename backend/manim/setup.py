import anthropic
from prompts import (CONCEPT_BREAKDOWN, ANIMATION_TESTING, DESIGN, 
                   CODE_GENERATION, 
                   extract_code_only, extract_section)

class ManimGenerator:
    def __init__(self, api_key=None):
        print(f"Debug: Initializing ManimGenerator with API key length: {len(api_key) if api_key else 0}")
        print(f"Debug: API key starts with: {api_key[:12] if api_key else 'None'}")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-7-sonnet-20250219"
        print(f"Initialized ManimGenerator with model: {self.model}")
    
    def _send_prompt(self, prompt, max_tokens=5000):
        """Helper method to send a prompt to the API and get the text response"""
        print(f"Sending prompt to API with max_tokens={max_tokens}")
        print(f"Prompt first 100 chars: {prompt[:300]}...")
        print(f"Prompt last 100 chars: {prompt[-300:]}...")
        
        try:
            # Add debug info about the client and API key
            print(f"Debug: Client initialized: {self.client is not None}")
            print(f"Debug: API key length: {len(self.client.api_key) if self.client and hasattr(self.client, 'api_key') else 'N/A'}")
            print(f"Debug: API key starts with: {self.client.api_key[:12] if self.client and hasattr(self.client, 'api_key') else 'N/A'}")
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Get the text content from the response
            content_text = ""
            for content_block in message.content:
                if content_block.type == "text":
                    content_text += content_block.text
            
            print(f"Received response of length: {len(content_text)}")
            print(f"Response first 100 chars: {content_text[:100]}...")
            print(f"Response last 100 chars: {content_text[-100:]}...")
            
            # Check for <CODE_START> and <CODE_END> tags
            if "<CODE_START>" in content_text and "<CODE_END>" in content_text:
                print("SUCCESS: Found <CODE_START> and <CODE_END> tags in response")
            else:
                print("WARNING: <CODE_START> or <CODE_END> tags not found in response")
                # Print snippets around potential code areas
                if "```python" in content_text:
                    print("Found '```python' in response - checking context:")
                    index = content_text.find("```python")
                    context_start = max(0, index - 50)
                    context_end = min(len(content_text), index + 50)
                    print(f"Context around ```python: {content_text[context_start:context_end]}")
                
                if "```" in content_text:
                    print(f"Found {content_text.count('```')} occurrences of ``` in response")
            
            return content_text
        except Exception as e:
            print(f"Error sending prompt: {str(e)}")
            print(f"Error type: {type(e)}")
            print(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details available'}")
            return None
    
    def analyze_concept(self, math_topic, audience_level="high school"):
        """Break down a mathematical concept for visualization"""
        print(f"\n[STEP 1] Analyzing concept: {math_topic} for {audience_level} audience")
        formatted_prompt = CONCEPT_BREAKDOWN.format(
            topic=math_topic,
            audience_level=audience_level
        )
        response = self._send_prompt(formatted_prompt, max_tokens=3500)
        
        # Extract the key sections from the response
        concept_analysis = extract_section(response, "concept_analysis")
        visualization_approach = extract_section(response, "visualization_approach")
        key_visual_elements = extract_section(response, "key_visual_elements")
        
        print(f"Extracted concept_analysis: {len(concept_analysis) if concept_analysis else 0} chars")
        print(f"Extracted visualization_approach: {len(visualization_approach) if visualization_approach else 0} chars")
        print(f"Extracted key_visual_elements: {len(key_visual_elements) if key_visual_elements else 0} chars")
        
        return {
            "concept_analysis": concept_analysis,
            "visualization_approach": visualization_approach,
            "key_visual_elements": key_visual_elements,
            "full_response": response
        }
    
    def design_scene(self, math_topic, audience_level="high school", concept_analysis=None):
        """Generate an animation design for a given math topic"""
        print(f"\n[STEP 2] Designing scene for: {math_topic}")
        formatted_prompt = DESIGN.format(
            topic=math_topic,
            audience_level=audience_level
        )
        
        # If we have a concept analysis, include it in the prompt
        if concept_analysis:
            formatted_prompt += f"\n\n<concept_analysis>\n{concept_analysis}\n</concept_analysis>"
            print("Included concept_analysis in design prompt")
        
        response = self._send_prompt(formatted_prompt, max_tokens=3500)
        
        # Extract the animation design section
        animation_design = extract_section(response, "animation_design")
        self_evaluation = extract_section(response, "self_evaluation")
        
        print(f"Extracted animation_design: {len(animation_design) if animation_design else 0} chars")
        print(f"Extracted self_evaluation: {len(self_evaluation) if self_evaluation else 0} chars")
        
        return {
            "animation_design": animation_design,
            "self_evaluation": self_evaluation,
            "full_response": response
        }
    
    def test_animation_design(self, math_topic, animation_design):
        """Test an animation design for potential issues"""
        print(f"\n[STEP 3] Testing animation design for: {math_topic}")
        formatted_prompt = ANIMATION_TESTING.format(
            topic=math_topic,
            animation_design=animation_design
        )
        
        response = self._send_prompt(formatted_prompt, max_tokens=3000)
        
        # Extract the key sections
        novice_viewer = extract_section(response, "novice_viewer")
        expert_viewer = extract_section(response, "expert_viewer")
        cognitive_load = extract_section(response, "cognitive_load_analysis")
        improvements = extract_section(response, "design_improvements")
        
        print(f"Extracted novice_viewer: {len(novice_viewer) if novice_viewer else 0} chars")
        print(f"Extracted expert_viewer: {len(expert_viewer) if expert_viewer else 0} chars")
        print(f"Extracted cognitive_load: {len(cognitive_load) if cognitive_load else 0} chars")
        print(f"Extracted improvements: {len(improvements) if improvements else 0} chars")
        
        return {
            "novice_viewer": novice_viewer,
            "expert_viewer": expert_viewer,
            "cognitive_load": cognitive_load,
            "improvements": improvements,
            "full_response": response
        }
    
    def generate_code(self, design, topic):
        """Generate Manim code based on the design"""
        print(f"\n[STEP 4] Generating code for: {topic}")
        # Create a safe class name for the topic
        safe_class_name = ''.join(word.title() for word in topic.split()) + 'Scene'
        print(f"Using safe class name: {safe_class_name}")
        
        # Format the prompt with topic and design
        formatted_prompt = CODE_GENERATION.format(
            topic=topic,
            design_scene=design,
            safe_class_name=safe_class_name,
            TOPIC=topic,  # Added for template compatibility
            SAFE_CLASS_NAME=safe_class_name  # Added for template compatibility
        )
        
        # Add debug info directly to prompt
        formatted_prompt += "\n\nIMPORTANT DEBUG NOTE: The system REQUIRES you to include EXACT <CODE_START> and <CODE_END> tags around your code. DO NOT use markdown triple backticks or any variations. The format must be exactly as shown in the example with unmodified tags."
        
        print("Sending code generation prompt with debug note added")
        response = self._send_prompt(formatted_prompt, max_tokens=5000)
        
        # Debug the raw response
        print("\nDEBUG: Checking raw response for code tags:")
        if "<CODE_START>" in response:
            start_idx = response.find("<CODE_START>")
            print(f"Found <CODE_START> tag at position {start_idx}")
            print(f"Content around start tag: {response[max(0, start_idx-20):start_idx+20]}")
        else:
            print("ERROR: <CODE_START> tag not found in response")
            
        if "<CODE_END>" in response:
            end_idx = response.find("<CODE_END>")
            print(f"Found <CODE_END> tag at position {end_idx}")
            print(f"Content around end tag: {response[max(0, end_idx-20):end_idx+20]}")
        else:
            print("ERROR: <CODE_END> tag not found in response")
        
        # Check for code blocks in markdown format
        if "```python" in response:
            py_start = response.find("```python")
            py_end = response.find("```", py_start + 10)
            print(f"Found markdown python block: positions {py_start} to {py_end}")
            print(f"First 100 chars of markdown block: {response[py_start+10:py_start+110]}...")
        
        # Extract only the code portion, with topic validation
        print("Attempting to extract code with topic validation")
        clean_code = extract_code_only(response, topic)
        print(f"Extracted code length: {len(clean_code) if clean_code else 0} chars")
        
        self_evaluation = extract_section(response, "code_self_evaluation")
        print(f"Extracted self_evaluation: {len(self_evaluation) if self_evaluation else 0} chars")
        
        # Handle case where code extraction or topic validation failed
        if not clean_code:
            print(f"\nERROR: Failed to extract valid code for topic '{topic}'")
            print("The generated code may not be relevant to the requested topic.")
            print("Attempting to prompt Claude again with stronger topic emphasis...")
            
            # Try again with even stronger topic emphasis
            retry_prompt = CODE_GENERATION.format(
                topic=topic,
                design_scene=design,
                safe_class_name=safe_class_name,
                TOPIC=topic,
                SAFE_CLASS_NAME=safe_class_name
            )
            retry_prompt += f"\n\nCRITICAL: You MUST create a MANIM animation about {topic}. " \
                        f"The class name should include '{topic.replace(' ', '')}' and " \
                        f"the code must explicitly be about {topic} in its comments and visuals."
            
            retry_prompt += "\n\nABSOLUTELY CRITICAL: You MUST wrap your code in <CODE_START> and <CODE_END> tags EXACTLY as shown below. DO NOT use markdown formatting, DO NOT use triple backticks, ONLY use these exact tags:\n\n<CODE_START>\n# Your code here\n<CODE_END>"
            
            print("Sending retry prompt with CRITICAL tag instructions")
            retry_response = self._send_prompt(retry_prompt, max_tokens=5000)
            
            print("\nDEBUG: Checking retry response for code tags:")
            if "<CODE_START>" in retry_response:
                start_idx = retry_response.find("<CODE_START>")
                print(f"Found <CODE_START> tag at position {start_idx}")
            else:
                print("ERROR: <CODE_START> tag still not found in retry response")
                
            if "<CODE_END>" in retry_response:
                end_idx = retry_response.find("<CODE_END>")
                print(f"Found <CODE_END> tag at position {end_idx}")
            else:
                print("ERROR: <CODE_END> tag still not found in retry response")
            
            clean_code = extract_code_only(retry_response, topic)
            print(f"Extracted code from retry: {len(clean_code) if clean_code else 0} chars")
            
            if not clean_code:
                print("ERROR: Still failed to generate relevant code after retry.")
                return {
                    "code": None,
                    "self_evaluation": None,
                    "full_response": response,
                    "error": f"Failed to generate code relevant to '{topic}'"
                }
        
        return {
            "code": clean_code,
            "self_evaluation": self_evaluation,
            "full_response": response
        }
    
    def complete_workflow(self, math_topic, audience_level="high school"):
        """Run the complete animation generation workflow"""
        print(f"\n[WORKFLOW] Starting complete workflow for topic: {math_topic}")
        
        # Step 1: Analyze the concept
        print("Step 1/5: Analyzing mathematical concept...")
        concept_results = self.analyze_concept(math_topic, audience_level)
        print("Concept analysis completed successfully!")
        
        # Step 2: Design the animation
        print("Step 2/5: Generating animation design...")
        design_results = self.design_scene(
            math_topic, 
            audience_level, 
            concept_results["concept_analysis"]
        )
        print("Animation design generated successfully!")
        
        # Step 3: Test the animation design
        print("Step 3/5: Testing animation design for improvements...")
        test_results = self.test_animation_design(
            math_topic,
            design_results["animation_design"]
        )
        print("Design testing completed successfully!")
        
        # Step 4: Generate code based on design and test feedback
        print("Step 4/5: Generating Manim code...")
        enhanced_design = design_results["animation_design"] + "\n\n" + test_results["improvements"]
        code_results = self.generate_code(enhanced_design, math_topic)
        
        if code_results.get("code"):
            print("Code generated successfully!")
            print(f"Generated code for '{math_topic}':")
            print("----------------------------------------")
            # Print first few lines of code
            code_lines = code_results["code"].split("\n")
            for i, line in enumerate(code_lines[:10]):
                print(line)
            if len(code_lines) > 10:
                print("...")
            print("----------------------------------------")
        else:
            print(f"Failed to generate code for '{math_topic}'")
        
        # Check for missing components or handle incomplete workflow
        final_code = code_results.get("code")
        summary = "Workflow completed successfully" if final_code else "Workflow incomplete - no valid code generated"
        
        return {
            "concept_analysis": concept_results,
            "animation_design": design_results,
            "design_testing": test_results,
            "code_generation": code_results,
            "final_code": final_code,
            "summary": summary
        }