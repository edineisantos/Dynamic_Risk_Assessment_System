from flask import Flask, jsonify
import json
import pandas as pd
import os
from diagnostics import (
    model_predictions,
    dataframe_summary,
    execution_time,
    percent_missing_values,
    outdated_packages_list
)
from scoring import score_model


# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json', 'r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')
output_model_path = config['output_model_path']  # Define model path

# Prediction Endpoint


@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    # Call the model_predictions function to get predictions
    predictions = model_predictions(
        model_path=os.path.join(output_model_path, 'trainedmodel.pkl'),
        test_data_path=test_data_path)

    # Return predictions as JSON
    return jsonify(predictions.tolist())

# Scoring Endpoint


@app.route("/scoring", methods=['GET', 'OPTIONS'])
def scoring_f1():
    # Call the score_model function to check the score of the deployed model
    score_model()

    # Load the F1 score from 'latestscore.txt'
    score_path = os.path.join(output_model_path, 'latestscore.txt')

    # Read the F1 score from the file
    with open(score_path, 'r') as score_file:
        f1_score = float(score_file.read())

    # Return the F1 score as JSON
    return jsonify({'f1_score': f1_score})

# Summary Statistics Endpoint


@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats():
    # Call the dataframe_summary function to calculate summary statistics
    summary_stats = dataframe_summary()

    # Convert the summary statistics to a dictionary for JSON response
    summary_dict = summary_stats.to_dict()

    # Return the calculated summary statistics as JSON
    return jsonify(summary_dict)

# Diagnostics Endpoint


@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnostics_api():        
    # Call the functions for timing, missing data, and dependency check
    timing_results = execution_time()
    missing_data_results = percent_missing_values()
    dependency_check_results = outdated_packages_list()

    # Create a dictionary to store the diagnostic results
    diagnostics_results = {
        "timing": {
            "ingestion_time": timing_results[0],
            "training_time": timing_results[1]
        },
        "missing_data_percent": missing_data_results,
        "dependency_check": dependency_check_results
    }

    # Convert any Pandas Series to dictionaries
    for key, value in diagnostics_results.items():
        if isinstance(value, pd.Series):
            diagnostics_results[key] = value.to_dict()

    # Return the diagnostic results as JSON
    return jsonify(diagnostics_results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8890, debug=True, threaded=True)
