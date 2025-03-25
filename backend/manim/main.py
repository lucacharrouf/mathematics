from dotenv import load_dotenv
import os
import argparse
import requests
import json
import re
import traceback
from generate_video import VideoGenerator

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate Manim animations for math concepts")
    parser.add_argument("--topic", type=str, required=True, help="Mathematical topic to animate")
    parser.add_argument("--audience", type=str, default="high school", 
                      help="Target audience level (e.g., elementary, middle school, high school, undergraduate)")
    parser.add_argument("--feedback", type=str, default=None, 
                      help="Path to a text file containing user feedback for improving an existing animation")
    parser.add_argument("--server-url", type=str, default="http://localhost:4000", 
                      help="URL of the Node.js server")
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
    
    # Process user feedback if provided
    user_feedback = None
    if args.feedback and os.path.exists(args.feedback):
        try:
            with open(args.feedback, 'r') as feedback_file:
                user_feedback = feedback_file.read()
            print(f"Loaded user feedback from {args.feedback}")
        except Exception as e:
            print(f"Error reading feedback file: {e}")
    
    # Generate the video with complete workflow
    result = video_gen.generate_video(args.topic, args.audience, user_feedback)
    success = isinstance(result, str) 
    
    # Save result to MongoDB via the Express server
    try:
        # Read the generated code
        code_content = ""
        video_path = ""
        
        if success:
            # Extract the code filename from the video path
            video_path = result
            safe_topic = os.path.basename(video_path).replace('_animation.mp4', '')
            code_filename = f"generated_{safe_topic}.py"
            code_path = os.path.join(video_gen.code_dir, code_filename)
            
            if os.path.exists(code_path):
                with open(code_path, 'r') as file:
                    code_content = file.read()
                print(f"Successfully read code from: {code_path}")
            else:
                print(f"Code file not found at: {code_path}")
        else:
            print(f"Video generation failed, no code to read")
        
        # Test server connection before sending data
        try:
            test_response = requests.get(args.server_url)
            print(f"Test connection to server root - Status: {test_response.status_code}")
            if test_response.status_code != 200:
                print(f"Warning: Server is not responding correctly. Response: {test_response.text}")
        except Exception as test_err:
            print(f"Test connection failed: {str(test_err)}")
            print("Make sure your Node.js server is running")
            
        # Prepare data to send to the server
        data = {
            "topic": args.topic,
            "audience": args.audience,
            "code": code_content,
            "status": "completed" if success else "failed",
            "videoPath": video_path if success and os.path.exists(video_path) else "",
            "hasFeedback": user_feedback is not None
        }
        
        endpoint_url = f"{args.server_url}/videos/save-from-python"
        print(f"Attempting to send data to: {endpoint_url}")
        print(f"Data length - Topic: {len(data['topic'])}, Code: {len(data['code'])}")
        print(f"Video path: {data['videoPath']}")
        
        # Send data to the server
        response = requests.post(
            endpoint_url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30  # Longer timeout for processing video files
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 201:
            print("Successfully saved data to the database")
            try:
                resp_data = response.json()
                print(f"Saved video ID: {resp_data.get('data', {}).get('_id', 'unknown')}")
            except:
                pass
        else:
            print(f"Failed to save data to database. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error: {str(conn_err)}")
        print("Is the server running at the specified URL?")
    except requests.exceptions.Timeout:
        print(f"Request timed out. Server might be busy or unreachable.")
    except Exception as e:
        print(f"Error communicating with the server: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Display completion message
    if success:
        print(f"\nProcess completed for topic: '{args.topic}'")
        print(f"Code saved to: {video_gen.code_dir}")
        print(f"Artifacts saved to: {os.path.join(video_gen.videos_dir, os.path.basename(video_path).replace('_animation.mp4', '') + '_artifacts')}")
        if isinstance(result, str):
            print(f"Video saved to: {result}")
    else:
        print(f"\nFailed to complete the process for topic: '{args.topic}'")

if __name__ == "__main__":
    main()