import os
import requests
import json

# Specify a URL that resolves to your workspace
BASE_URL = "http://0.0.0.0:8890/"

# Define the API endpoints
PREDICTION_ENDPOINT = BASE_URL + "prediction"
SCORING_ENDPOINT = BASE_URL + "scoring"
SUMMARY_STATS_ENDPOINT = BASE_URL + "summarystats"
DIAGNOSTICS_ENDPOINT = BASE_URL + "diagnostics"

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

# Test data path
test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')

# Output directory path
output_model_path = config['output_model_path']

# Call each API endpoint and store the responses
response1 = requests.post(PREDICTION_ENDPOINT,
                          json={"test_data_path": test_data_path})
response2 = requests.get(SCORING_ENDPOINT)
response3 = requests.get(SUMMARY_STATS_ENDPOINT)
response4 = requests.get(DIAGNOSTICS_ENDPOINT)

# Combine all API responses
responses = {
    "prediction": response1.json(),
    "scoring": response2.json(),
    "summary_stats": response3.json(),
    "diagnostics": response4.json()
}

# Define the path for apireturns.txt in the output_model_path directory
apireturns_path = os.path.join(output_model_path, "apireturns.txt")

# Write the responses to the apireturns.txt file
with open(apireturns_path, "w") as outfile:
    json.dump(responses, outfile, indent=4)
