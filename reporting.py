import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

# Default test data and output model paths
default_test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')
default_output_model_path = config['output_model_path']

# Function for reporting


def score_model(test_data_file=default_test_data_path,
                model_predictions_file=None):
    # Use the model_predictions function to get predictions
    if model_predictions_file is None:
        predictions = model_predictions()
    else:
        predictions = model_predictions(model_path=model_predictions_file,
                                        test_data_path=test_data_file)

    # Load the test data
    test_data = pd.read_csv(test_data_file)

    # Separate the y_test data (exited) from the test_data
    y_test = test_data['exited']

    # Generate a confusion matrix
    confusion_matrix = metrics.confusion_matrix(y_test, predictions)

    # Plot the confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')

    # Save the confusion matrix plot to the output model path
    if model_predictions_file is None:
        plt.savefig(os.path.join(default_output_model_path,
                                 'confusionmatrix.png'))
    else:
        output_dir = os.path.dirname(model_predictions_file)
        plt.savefig(os.path.join(output_dir, 'confusionmatrix.png'))


if __name__ == '__main__':
    score_model()
