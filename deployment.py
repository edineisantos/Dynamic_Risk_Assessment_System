import os
import json
import shutil

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'], 'trainedmodel.pkl')
score_path = os.path.join(config['output_model_path'], 'latestscore.txt')
ingested_files_path = os.path.join(config['output_folder_path'],
                                   'ingestedfiles.txt')

# Function for model deployment


def deploy_model():
    # Copy trained model to the production deployment directory
    shutil.copy(model_path, os.path.join(prod_deployment_path,
                                         'trainedmodel.pkl'))

    # Copy model score to the production deployment directory
    shutil.copy(score_path, os.path.join(prod_deployment_path,
                                         'latestscore.txt'))

    # Copy ingested files record to the production deployment directory
    shutil.copy(ingested_files_path, os.path.join(prod_deployment_path,
                                                  'ingestedfiles.txt'))


if __name__ == '__main__':
    deploy_model()
