import os
import json
import pickle
import pandas as pd
from sklearn import metrics

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

model_folder_path = config['output_model_path']
test_data_folder_path = config['test_data_path']

# Default filenames for the model and test data
default_model_filename = 'trainedmodel.pkl'
default_test_data_filename = 'testdata.csv'

# Function for model scoring


def score_model(trained_model=None, test_data_filename=None):
    # If trained_model or test_data_filename is not provided,
    # use default values
    if trained_model is None:
        trained_model_path = os.path.join(model_folder_path,
                                          default_model_filename)
    else:
        trained_model_path = os.path.join(model_folder_path, trained_model)

    if test_data_filename is None:
        test_data_path = os.path.join(test_data_folder_path,
                                      default_test_data_filename)
    else:
        test_data_path = os.path.join(test_data_folder_path,
                                      test_data_filename)

    # Load the trained model
    with open(trained_model_path, 'rb') as model_file:
        trained_model = pickle.load(model_file)

    # Load test data
    test_data = pd.read_csv(test_data_path)

    # Separate predictors (features) and target variable
    X_test = test_data[['lastmonth_activity', 'lastyear_activity',
                        'number_of_employees']]
    y_test = test_data['exited']

    # Predict using the trained model
    y_pred = trained_model.predict(X_test)

    # Calculate the F1 score
    f1_score = metrics.f1_score(y_test, y_pred)

    # Write the F1 score to 'latestscore.txt'
    score_path = os.path.join(model_folder_path, 'latestscore.txt')
    with open(score_path, 'w') as score_file:
        score_file.write(str(f1_score))


if __name__ == '__main__':
    score_model()
