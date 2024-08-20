import openai
import json

# Load input data from input.json
with open('input.json') as f:
    input_data = json.load(f)

# OpenAI API initialization (replace 'your_openai_api_key' with your actual API key)
openai.api_key = 'your_openai_api_key'

def generate_response(profile_context, latest_query, chat_context):
    # Extract useful information
    patient_profile = profile_context['patient_profile']
    diet_chart = profile_context['diet_chart']
    
    # Create a prompt for LLM
    prompt = f"""
    You are a healthcare AI specializing in dietary management. 
    You have the following patient information:
    
    Patient profile: {patient_profile}
    Diet chart: {diet_chart}

    The patient just sent a message: {latest_query[-1]['message']}

    Please analyze the message, understand the context from the chat history, 
    and provide an appropriate, personalized response based on their diet and medical conditions.
    """

    # Call OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Iterate through patient queries and generate responses
output_data = []

for query_obj in input_data:
    ticket_id = query_obj['chat_context']['ticket_id']
    latest_query = query_obj['latest_query']
    ideal_response = query_obj['ideal_response']
    
    # Generate response using LLM
    generated_response = generate_response(query_obj['profile_context'], latest_query, query_obj['chat_context'])

    # Save result
    output_data.append({
        'ticket_id': ticket_id,
        'latest_query': latest_query,
        'generated_response': generated_response,
        'ideal_response': ideal_response
    })

# Save output data to JSON file
with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Responses generated and saved to output.json")
