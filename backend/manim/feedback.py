from dotenv import load_dotenv
import os
import argparse
import requests
import json
import sys

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Provide feedback for math concept animations")
    parser.add_argument("--topic", type=str, required=True, help="Mathematical topic to provide feedback for")
    parser.add_argument("--server-url", type=str, default="http://localhost:4000", 
                      help="URL of the Node.js server")
    parser.add_argument("--rating", type=int, help="Rating from 1-5 (optional)")
    args = parser.parse_args()
    
    print(f"Server URL: {args.server_url}")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Validate rating if provided
    if args.rating is not None and (args.rating < 1 or args.rating > 5):
        print("Error: Rating must be between 1 and 5")
        return
    
    # Prompt the user for feedback
    print(f"\nProviding feedback for topic: '{args.topic}'")
    if args.rating:
        print(f"Rating: {args.rating}/5")
    else:
        print("No rating provided")
        
    print("\nEnter your feedback below (press Ctrl+D or Ctrl+Z on Windows when finished):")
    
    # Read multiline input from the user
    feedback_lines = []
    try:
        while True:
            try:
                line = input()
                feedback_lines.append(line)
            except EOFError:
                # User pressed Ctrl+D (Unix)
                break
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\nInput interrupted.")
        return
    
    feedback = "\n".join(feedback_lines)
    
    if not feedback.strip():
        print("No feedback provided. Exiting.")
        return
    
    # Save feedback to MongoDB via the Express server
    try:
        # Test server connection before sending data
        try:
            test_response = requests.get(args.server_url)
            print(f"Test connection to server root - Status: {test_response.status_code}")
            if test_response.status_code != 200:
                print(f"Warning: Server is not responding correctly. Response: {test_response.text}")
        except Exception as test_err:
            print(f"Test connection failed: {str(test_err)}")
            print("Make sure your Node.js server is running")
            return
            
        # Prepare data to send to the server
        data = {
            "topic": args.topic,
            "feedback": feedback
        }
        
        # Add rating if provided
        if args.rating is not None:
            data["rating"] = args.rating
        
        # Using the existing input endpoint instead of a dedicated feedback endpoint
        endpoint_url = f"{args.server_url}/input/update-feedback"
        print(f"Attempting to send feedback to: {endpoint_url}")
        
        # Send data to the server
        response = requests.post(
            endpoint_url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("Successfully saved feedback to the database")
        else:
            print(f"Failed to save feedback to database. Status code: {response.status_code}")
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

if __name__ == "__main__":
    main()