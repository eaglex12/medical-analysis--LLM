import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API key is missing! Please ensure it's set in your .env file as OPENAI_KEY.")

def generate_response(profile_context, latest_query, chat_context):
    patient_profile = profile_context.get('patient_profile', 'No profile available')
    diet_chart = profile_context.get('diet_chart', 'No diet chart available')
    
    if not latest_query:
        return "Unable to generate response, no latest query found."

    last_message = latest_query[-1].get('message', 'No message found')

    prompt = f"""
    You are a healthcare AI specializing in dietary management. 
    You have the following patient information:
    
    Patient profile: {patient_profile}
    Diet chart: {diet_chart}

    The patient just sent a message: {last_message}

    Please analyze the message, understand the context from the chat history, 
    and provide an appropriate, personalized response based on their diet and medical conditions.
    """

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,  
            stop=["\n"]  #
        )

        return response.choices[0].text.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"

try:
    with open('input.json') as f:
        input_data = json.load(f)
except FileNotFoundError:
    print("input.json file not found.")
    exit(1)

output_data = []

for query_obj in input_data:
    ticket_id = query_obj['chat_context'].get('ticket_id', 'No ticket ID')
    latest_query = query_obj.get('latest_query', [])
    ideal_response = query_obj.get('ideal_response', 'No ideal response provided')

    generated_response = generate_response(query_obj['profile_context'], latest_query, query_obj['chat_context'])

    output_data.append({
        'ticket_id': ticket_id,
        'latest_query': latest_query,
        'generated_response': generated_response,
        'ideal_response': ideal_response
    })

with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Responses generated and saved to output.json")
