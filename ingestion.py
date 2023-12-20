import pandas as pd
import os
import json

# Load config.json and get input and output paths
with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']

# Function for data ingestion


def merge_multiple_dataframe():
    # Initialize an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    # List all CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder_path)
                 if file.endswith(".csv")]

    # Loop through CSV files and combine data
    for csv_file in csv_files:
        file_path = os.path.join(input_folder_path, csv_file)

        # Print the file being read
        print(f"Reading the file: {csv_file} ...")

        temp_df = pd.read_csv(file_path)
        combined_data = pd.concat([combined_data, temp_df], ignore_index=True)

    # Remove duplicate rows
    combined_data = combined_data.drop_duplicates()

    # Save the ingested data as a CSV file
    output_file_path = os.path.join(output_folder_path, "finaldata.csv")
    combined_data.to_csv(output_file_path, index=False)

    # Record the names of ingested files for tracking
    ingested_file_list = csv_files

    # Save the record of ingested files to ingestedfiles.txt
    ingested_files_path = os.path.join(output_folder_path, "ingestedfiles.txt")
    with open(ingested_files_path, "w") as ingested_file:
        for file_name in ingested_file_list:
            ingested_file.write(file_name + "\n")


if __name__ == '__main__':
    merge_multiple_dataframe()
