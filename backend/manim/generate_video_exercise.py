import os
import subprocess
import re
import shutil
from setup import ManimGenerator
from prompts_exercise import process_math_visualization_request

class VideoGenerator:
    def __init__(self, api_key):
        # Create directories in the user's home directory
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.code_dir = os.path.join(curr_dir, "content", "code_dir")
        self.videos_dir = os.path.join(curr_dir, "content", "videos_dir")
        
        # Create necessary directories
        os.makedirs(self.code_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)
        
        # Initialize generator with API key
        self.generator = ManimGenerator(api_key=api_key)
    
    def _get_safe_filename(self, math_topic):
        """Convert math topic to a safe filename"""
        return math_topic.lower().replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_')
        
    def _extract_class_name(self, code):
        """Extract the class name from the generated code"""
        class_match = re.search(r'class\s+(\w+)\s*\(Scene\)', code)
        if class_match:
            return class_match.group(1)
        return "MathAnimation"  # Default class name

    def generate_video_from_code(self, code_path, topic):
        """Generate a video from an existing code file"""
        try:
            # Extract the class name from the code file
            with open(code_path, 'r') as f:
                code = f.read()
            class_name = self._extract_class_name(code)
            
            # Create output directories
            temp_media_dir = os.path.join(self.code_dir, "media")
            os.makedirs(temp_media_dir, exist_ok=True)
            
            # Change to the code directory to run manim
            original_dir = os.getcwd()
            os.chdir(self.code_dir)
            
            print(f"Running Manim animation...")
            
            # Run Manim with low quality for speed (-ql)
            result = subprocess.run(
                ['manim', '-ql', code_path, class_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Manim error: {result.stderr}")
                os.chdir(original_dir)
                return False
                
            # Find the generated video file
            video_pattern = r"File ready at '(.*?)'"
            match = re.search(video_pattern, result.stdout)
            
            if match:
                source_path = match.group(1)
            else:
                # Look in media directory for the most recent mp4
                media_videos_dir = os.path.join(temp_media_dir, "videos", 
                    os.path.basename(code_path).replace('.py', ''), "480p15")
                if os.path.exists(media_videos_dir):
                    mp4_files = [f for f in os.listdir(media_videos_dir) if f.endswith('.mp4')]
                    if mp4_files:
                        mp4_files.sort(key=lambda x: os.path.getctime(
                            os.path.join(media_videos_dir, x)), reverse=True)
                        source_path = os.path.join(media_videos_dir, mp4_files[0])
                    else:
                        print("No MP4 files found")
                        os.chdir(original_dir)
                        return False
                else:
                    print(f"Media directory not found: {media_videos_dir}")
                    os.chdir(original_dir)
                    return False
            
            # Copy to videos directory with a descriptive name
            safe_topic = self._get_safe_filename(topic)
            target_filename = f"{safe_topic}_animation.mp4"
            target_path = os.path.join(self.videos_dir, target_filename)
            
            shutil.copy2(source_path, target_path)
            print(f"Animation saved to {target_path}")
            
            # Change back to original directory
            os.chdir(original_dir)
            
            return target_path
            
        except Exception as e:
            print(f"Error generating video: {e}")
            if 'original_dir' in locals():
                os.chdir(original_dir)
            return False

    def generate_video(self, math_topic, audience_level="high school", user_feedback=None):
        """Generate a Manim animation video for the given math topic"""
        print(f"Starting video generation for topic: {math_topic}")
        
        # Define the LLM response function
        def get_llm_response(prompt):
            return self.generator._send_prompt(prompt)

        # Process the visualization request using the enhanced prompt system
        print(f"\nProcessing visualization request...")
        visualization_result = process_math_visualization_request(
            query=math_topic,
            audience_level=audience_level,
            get_llm_response_func=get_llm_response
        )
        
        if not visualization_result['success']:
            print("Failed to process visualization request")
            return False

        # Extract the code
        code = visualization_result['code']
        if not code:
            print("No code was generated")
            return False
            
        # Create safe filename
        safe_topic = self._get_safe_filename(math_topic)
        filename = f"generated_{safe_topic}.py"
        filepath = os.path.join(self.code_dir, filename)
        
        # Save the code
        with open(filepath, 'w') as file:
            file.write(code)
        
        print(f"Code saved to {filepath}")
        
        # Generate the video
        return self.generate_video_from_code(filepath, math_topic)
