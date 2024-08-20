import openai
from dotenv import load_dotenv, get_key

# Load environment variables from .env
load_dotenv()

# Get the OpenAI API key
openai.api_key = get_key('.env', 'OPENAI_KEY')

# Test function to check if OpenAI API is responding
def test_openai_response():
    try:
        # Example prompt for testing
        prompt = "Say hello!"
        
        # Request to OpenAI API
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=10
        )
        
        # Print the response
        print("OpenAI Response:", response.choices[0].text.strip())
    
    except Exception as e:
        print("Error connecting to OpenAI:", e)

# Run the test
test_openai_response()
