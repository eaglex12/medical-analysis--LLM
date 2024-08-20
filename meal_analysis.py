import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API
api_key = os.getenv("GEM")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")
genai.configure(api_key=api_key)

# Initialize the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_name_from_ideal_response(ideal_response):
    """
    Extract the patient name from the ideal_response text.
    Assumes the name is mentioned after a specific pattern, e.g., 'Varsha'.
    """
    # Improved pattern to find names; assumes names are capitalized
    matches = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b', ideal_response)
    return matches[0] if matches else 'Patient'

def generate_response(profile_context, latest_query, chat_context, patient_name):
    patient_profile = profile_context.get('patient_profile', 'No profile available')
    diet_chart = profile_context.get('diet_chart', 'No diet chart available')

    if not latest_query:
        return "Unable to generate response, no latest query found."

    last_message = latest_query[-1].get('content', 'No message found')

    prompt = f"""
You are a healthcare AI specializing in dietary management, and your role is to provide personalized and supportive responses to patients based on their diet charts and recent activities. Your responses should:
    
    1. Acknowledge the patient's effort or actions in a positive tone.
2. Identify any deviations from the prescribed diet chart and ask the patient about the reasons for the deviation in a conversational, non-judgmental way.
3. Offer gentle reminders or advice on why adhering to the plan is important for their health goals, specifically related to their medical conditions such as PCOS or Hb levels.
4. Keep the response concise and personalized, addressing the patient by their name.
5. **Use Hinglish** (a mix of Hindi and English) where appropriate to make the conversation more relatable and friendly.


    Here is the patient's information:
    - **Patient Name**: {patient_name}
    - **Patient Profile**: {patient_profile}
    - **Diet Chart**: {diet_chart}

    Recent patient activities include:
    {latest_query}

    The latest message from the patient is:
    {last_message}

    Please generate a response that:
    1. **Acknowledges** the patient’s latest action or message.
    2. **Directly comments** on any deviation from the prescribed diet plan.
    3. **Uses specific and brief feedback** similar to this format:
        - "Shobhita, I noticed aap oats le rhe ho, which is a healthy choice, but maine aapki diet mein aloo parantha + curd likha tha, aapne vo nhi khaya?"
        - "Great job on following your diet plan, keep it up!"
        - "Rupa, I noticed that you were prescribed mixed veg vermicelli, can you let me know why you’re having idli?"
        - "Great job! I just checked, you are having sunflower and sesame seeds, but I mentioned pumpkin and flax seeds in your diet."
        - "Charleen, why are you having only paneer?"
        - "Aarti, aap konsi sabzi kha rhe ho?"
        - "Try to share a picture of the entire meal, so that we can review accordingly. Keep it up!"
    4. **Incorporate Hinglish** in the response when possible.

    5. **Ends with a supportive yet brief tone**.

    Keep the response short, specific, and clear, focusing on actionable feedback.
    """

    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    try:
        with open('input.json') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print("input.json file not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding input.json file.")
        return

    print("Generating responses, please wait...")
    output_data = []

    for query_obj in input_data:
        ticket_id = query_obj['chat_context'].get('ticket_id', 'No ticket ID')
        latest_query = query_obj.get('latest_query', [])
        ideal_response = query_obj.get('ideal_response', 'No ideal response provided')
        
        # Extract patient name from the ideal response
        patient_name = extract_name_from_ideal_response(ideal_response)
        
        generated_response = generate_response(query_obj['profile_context'], latest_query, query_obj['chat_context'], patient_name)

        output_data.append({
            'ticket_id': ticket_id,
            'latest_query': latest_query,
            'generated_response': generated_response,
            'ideal_response': ideal_response
        })

    try:
        with open('output.json', 'w') as f:
            json.dump(output_data, f, indent=4)
    except IOError as e:
        print(f"Error writing to output.json: {str(e)}")
        return

    print("Responses generated and saved to output.json")

if __name__ == "__main__":
    main()
