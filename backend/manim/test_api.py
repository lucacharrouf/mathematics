from dotenv import load_dotenv
import os
import anthropic

def test_api_key():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    print(f"Testing API key: {api_key[:12]}...")
    
    # Initialize the client
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        # Make a simple test request
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "Say hello"
            }]
        )
        print("API test successful!")
        print(f"Response: {message.content[0].text}")
    except Exception as e:
        print(f"API test failed: {str(e)}")

if __name__ == "__main__":
    test_api_key() 