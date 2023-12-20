import pandas as pd
import timeit
import os
import json
import pickle

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'], 'finaldata.csv')
test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'], 'trainedmodel.pkl')
score_path = os.path.join(config['output_model_path'], 'latestscore.txt')

# Function to get model predictions


def model_predictions(model_path=model_path, test_data_path=test_data_path):
    # Load the trained model
    with open(model_path, 'rb') as model_file:
        trained_model = pickle.load(model_file)

    # Load the test data
    test_data = pd.read_csv(test_data_path)

    # Extract predictors (features) from the test data
    X_test = test_data[['lastmonth_activity', 'lastyear_activity',
                        'number_of_employees']]

    # Make predictions using the trained model
    predictions = trained_model.predict(X_test)

    # Print the predicted values
    print('Predictions:')
    print(predictions)
    print("......................")

    return predictions

# Function to get summary statistics


def dataframe_summary(dataset_csv_path=dataset_csv_path):
    # Load the dataset
    dataset = pd.read_csv(dataset_csv_path)

    # Calculate summary statistics for numeric columns
    summary_stats = dataset.describe()

    # Print the summary statistics
    print('Summary statistics:')
    print(summary_stats)
    print("......................")

    return summary_stats


def percent_missing_values(dataset_csv_path=dataset_csv_path):
    # Load the dataset
    dataset = pd.read_csv(dataset_csv_path)

    # Calculate the percentage of missing values for each column
    missing_percentage = (dataset.isnull().sum() / len(dataset)) * 100

    # Print the percentage of missing values for each column
    print('Percentage of missing values for each column:')
    print(missing_percentage)
    print("......................")

    return missing_percentage

# Function to get timings


def execution_time():
    # Timing of data ingestion using ingestion.py
    ingestion_time = timeit.timeit(
        stmt='import ingestion; ingestion.merge_multiple_dataframe()',
        globals=globals(), number=1
    )
    # Print the time taken for ingestion
    print('Time taken for ingestion: ')
    print(ingestion_time)
    print("......................")

    # Timing of model training using training.py
    training_time = timeit.timeit(
        stmt='import training; training.train_model()',
        globals=globals(), number=1
    )
    # Print the time taken for training
    print('Time taken for training: ')
    print(training_time)
    print("......................")

    return [ingestion_time, training_time]


# Function to check dependencies
def outdated_packages_list():
    # Run a pip command to check for outdated packages
    pip_command = 'pip list --outdated --format=json'
    outdated_packages = os.popen(pip_command).read()

    # Parse the JSON output
    try:
        outdated_packages_json = json.loads(outdated_packages)
    except json.JSONDecodeError:
        print('Error: Failed to parse outdated packages information.')
        return None

    # Print the outdated packages one per line
    print('Outdated packages:')
    for package_info in outdated_packages_json:
        package_name = package_info["name"]
        current_version = package_info["version"]
        latest_version = package_info["latest_version"]
        print(
            f'{package_name} (Current Version: {current_version},'
            f'Latest Version: {latest_version})'
        )

    return outdated_packages


if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    percent_missing_values()
    execution_time()
    outdated_packages_list()
