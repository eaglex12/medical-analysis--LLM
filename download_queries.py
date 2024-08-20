import requests
import json

url = "https://clchatagentassessment.s3.ap-south-1.amazonaws.com/queries.json"

response = requests.get(url)

if response.status_code == 200:
    queries = response.json()
    
    with open('input.json', 'w') as f:
        json.dump(queries, f, indent=4)
    
    print("File 'input.json' has been successfully downloaded and saved.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
