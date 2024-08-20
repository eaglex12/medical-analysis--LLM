import requests
import json

# URL to download the sample queries
url = "https://clchatagentassessment.s3.ap-south-1.amazonaws.com/queries.json"

# Send a GET request to fetch the data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON content
    queries = response.json()
    
    # Save the JSON data to a file named input.json
    with open('input.json', 'w') as f:
        json.dump(queries, f, indent=4)
    
    print("File 'input.json' has been successfully downloaded and saved.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
