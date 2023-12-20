import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'], 'finaldata.csv')
model_path = os.path.join(config['output_model_path'], 'trainedmodel.pkl')

# Function for training the model


def train_model():
    # Read data from finaldata.csv
    data = pd.read_csv(dataset_csv_path)

    # Separate predictors (features) and target variable
    X = data[['lastmonth_activity', 'lastyear_activity',
              'number_of_employees']]
    y = data['exited']

    # Use the provided logistic regression model for training
    model = LogisticRegression(
        C=1.0, class_weight=None, dual=False, fit_intercept=True,
        intercept_scaling=1, l1_ratio=None, max_iter=100,
        multi_class='ovr', n_jobs=None, penalty='l2',
        random_state=0, solver='liblinear', tol=0.0001, verbose=0,
        warm_start=False
    )

    # Fit the logistic regression to your data
    model.fit(X, y)

    # Write the trained model in a file called trainedmodel.pkl
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)


if __name__ == '__main__':
    train_model()
