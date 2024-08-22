import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEM"))

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "Write a story about a magic backpack."

try:
    response = model.generate_content([prompt])
    print("Generated Response:")
    print(response.text.strip())
except Exception as e:
    print(f"Error generating content: {e}")
