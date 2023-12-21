import os
import sys
import json
from ingestion import merge_multiple_dataframe

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

prod_deployment_path = config['prod_deployment_path']
input_folder_path = config['input_folder_path']
ingested_files_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')

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
        new_data = True
    else:
        print("No new data found.")
        print("Terminating process.")
        sys.exit()  # Exit the script if no new data is found

# Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data


# Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here



# Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

# Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model


if __name__ == '__main__':
    print("Checking for new data...")
    ingest_new_data()
    print("Checking for model drift...")



