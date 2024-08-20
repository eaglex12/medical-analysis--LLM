import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEM"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(profile_context, latest_query, chat_context):
    patient_profile = profile_context.get('patient_profile', 'No profile available')
    diet_chart = profile_context.get('diet_chart', 'No diet chart available')
    patient_name = profile_context.get('name', 'Patient')

    if not latest_query:
        return "Unable to generate response, no latest query found."

    last_message = latest_query[-1].get('content', 'No message found')

    prompt = f"""
    You are a healthcare AI with expertise in dietary management. Your goal is to provide personalized feedback based on the patient’s profile and recent activities.

    Here is the patient's information:
    - **Patient Name**: {patient_name}
    - **Patient Profile**: {patient_profile}
    - **Diet Chart**: {diet_chart}

    Recent patient activities include:
    {latest_query}

    The latest message from the patient is:
    {last_message}

    Please generate a response that:
    1. **Acknowledges** the patient’s latest action or message positively, using their name.
    2. **Provides specific feedback** on any dietary deviations or comments related to the patient's recent messages or actions.
    3. **Offers practical advice** tailored to the patient’s diet and health goals, including any relevant suggestions or encouragement.
    4. **Maintains a supportive and professional tone** throughout the response.

    Ensure the response is clear and concise, directly addressing the patient’s situation and offering valuable guidance.
    """

    

    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

try:
    with open('input.json') as f:
        input_data = json.load(f)
except FileNotFoundError:
    print("input.json file not found.")
    exit(1)

print("Generating response, please wait...")
output_data = []

for query_obj in input_data:
    ticket_id = query_obj['chat_context'].get('ticket_id', 'No ticket ID')
    latest_query = query_obj.get('latest_query', [])
    profile_context = query_obj.get('profile_context', {})
    chat_context = query_obj.get('chat_context', {})

    generated_response = generate_response(profile_context, latest_query, chat_context)

    output_data.append({
        'ticket_id': ticket_id,
        'latest_query': latest_query,
        'generated_response': generated_response
    })

with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Responses generated and saved to output.json")
