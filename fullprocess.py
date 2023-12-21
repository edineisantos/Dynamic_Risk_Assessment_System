import os
import sys
import json
from ingestion import merge_multiple_dataframe
from scoring import score_model

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

prod_deployment_path = config['prod_deployment_path']
input_folder_path = config['input_folder_path']
ingested_files_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')
model_folder_path = config['output_model_path']
output_folder_path = config['output_folder_path']

# Function to check for new data
def check_for_new_data():
    # Read the list of ingested files
    ingested_files = set()
    if os.path.exists(ingested_files_path):
        with open(ingested_files_path, 'r') as ingested_file:
            for line in ingested_file:
                ingested_files.add(line.strip())
    print("Files that have been ingested:")
    print(ingested_files)

    # List files in the input folder
    input_files = os.listdir(input_folder_path)
    print("All files in the input folder:")
    print(input_files)

    # Find new files that need to be ingested
    new_files = [file for file in input_files if file not in ingested_files]

    return new_files

# Ingest new data if there are new files
def ingest_new_data():

    # Check for new data
    new_files = check_for_new_data()

    # Ingest new data
    if new_files:
        print("New data found:")
        print(new_files)
        print("Ingesting new data...")
        merge_multiple_dataframe()
        print("Ingestion completed.")
    else:
        print("No new data found.")
        print("Terminating process.")
        sys.exit()  # Exit the script if no new data is found

# Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
# Function to check for model drift
def check_for_model_drift():
    # Read the latest recorded score
    latest_score_path = os.path.join(prod_deployment_path, 'latestscore.txt')
    print("Latest score file path:", latest_score_path)
    if os.path.exists(latest_score_path):
        with open(latest_score_path, 'r') as latest_score_file:
            latest_score = float(latest_score_file.read().strip())
    else:
        print("Latest score file not found.")
        sys.exit()

    print("Latest recorded score:", latest_score)

    # Run scoring on the new data
    test_data_path = os.path.join(output_folder_path, 'finaldata.csv')
    print("Test data path:", test_data_path)
    production_model = os.path.join(prod_deployment_path, 'trainedmodel.pkl')
    print("Production model path:", production_model)
    new_score = score_model(trained_model=production_model, 
                            test_data_path=test_data_path)

    print("New score:", new_score)

    # Check for model drift
    if new_score < latest_score:
        print("Model drift detected. Proceeding with re-deployment.")
    else:
        print("No model drift detected. Ending the process.")
        sys.exit()  # Exit the script if no model drift is detected

# Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

# Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model


if __name__ == '__main__':
    print("Checking for new data...")
    ingest_new_data()
    print("Checking for model drift...")
    check_for_model_drift()


