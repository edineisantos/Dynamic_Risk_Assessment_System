import os
import json
import pickle
import pandas as pd
from sklearn import metrics

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')
model_path = os.path.join(config['output_model_path'], 'trainedmodel.pkl')
score_path = os.path.join(config['output_model_path'], 'latestscore.txt')

# Function for model scoring


def score_model():
    # Load the trained model from 'trainedmodel.pkl'
    with open(model_path, 'rb') as model_file:
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
    with open(score_path, 'w') as score_file:
        score_file.write(str(f1_score))


if __name__ == '__main__':
    score_model()
