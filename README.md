# Dynamic Risk Assessment system

## Project Overview
The Dynamic Risk Assessment Portfolio Project is a simplified demonstration of a machine learning pipeline for data ingestion, model monitoring, deployment, and reporting. It is designed to showcase the end-to-end process of building and maintaining machine learning models in a production-like environment. Please note that this project is for educational purposes and not intended for use in real production systems.

## Objectives
The key goals of this project include:

1. **Automated Risk Assessment:** Develop an automated system that can continuously assess and predict risks based on incoming data.

2. **Data Ingestion:** Implement a robust data ingestion process to collect data from diverse sources and prepare it for analysis.

3. **Model Training:** Train machine learning models on historical data to learn patterns and make predictions.

4. **Model Deployment:** Deploy the trained models into a production environment for real-time risk scoring.

5. **Model Monitoring:** Continuously monitor the deployed models for any signs of model drift or performance degradation.

6. **Reporting:** Generate reports and diagnostics to provide insights into the risk assessment results.

## File Structure Overview
The project directory structure is organized as follows:

- **/practicedata/:** Contains practice data used for testing and development.
- **/sourcedata/:** Contains the source data used for training machine learning models.
- **/ingesteddata/:** Stores compiled datasets after data ingestion.
- **/testdata/:** Contains additional data for testing machine learning models.
- **/models/:** Stores machine learning models intended for production use.
- **/practicemodels/:** Stores practice machine learning models.
- **/production_deployment/:** Holds final deployed machine learning models.

The key Python scripts in the project include:

- **training.py:** Script for training machine learning models.
- **scoring.py:** Script for scoring machine learning models.
- **deployment.py:** Script for deploying trained machine learning models.
- **ingestion.py:** Script for data ingestion.
- **diagnostics.py:** Script for measuring model and data diagnostics.
- **reporting.py:** Script for generating reports about model metrics.
- **app.py:** Script containing API endpoints.
- **wsgi.py:** Script to facilitate API deployment.
- **apicalls.py:** Script for making API calls.
- **fullprocess.py:** Script to determine the need for model redeployment and call other Python scripts as needed.

Additional project files:

- **config.json:** Configuration file specifying folder paths and script parameters.
- **cronjob.txt:** Cron job configuration file containing the command line for scheduled tasks.
- **cron_log.txt:** Log file for recording cron job execution.
- **Dockerfile:** Instructions for creating a Docker container for the project environment.

Certainly, you can include the step to run `app.py` to start the API service before running `fullprocess.py` or setting up the cron job. Here's the updated section:

## Running the Project

### Local Setup

To run this project locally, follow these steps:

1. Clone the project repository to your local machine.

2. Navigate to the project directory.

3. Ensure you have Python 3.8 installed.

4. Install the required Python packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Configure the `config.json` file to specify folder paths and other settings according to your environment. You can use the default values or change them as needed.

6. Start the API service by running the `app.py` script:

   ```bash
   python app.py
   ```

7. Run the project's main script `fullprocess.py` using Python:

   ```bash
   python fullprocess.py
   ```

### Using Docker

You can also run the project inside a Docker container. Docker provides a consistent and isolated environment for the project. Please note that you need to grant passwordless `sudo` access within the container for the cron job to work properly. Follow these steps:

1. Clone the project repository to your local machine.

2. Navigate to the project directory.

3. Build the Docker image using the provided `Dockerfile`:

   ```bash
   docker build -t dynamic_risk_assessment_system_image .
   ```

4. Run the Docker container, ensuring that you grant `sudo` access within the container. You can also customize the ports by replacing `8888:8888 -p 8889:8889 -p 8890:8890` with the desired ports:

   ```bash
   docker run --name dynamic_risk_assessment_system -p 8888:8888 -p 8889:8889 -p 8890:8890 -v ${PWD}:/home/jovyan/work/Dynamic_Risk_Assessment_System -e GRANT_SUDO=yes dynamic_risk_assessment_system_image
   ```

   Please note the addition of `-e GRANT_SUDO=yes` to allow `sudo` commands within the container. This is required for the cron job to execute successfully.

5. (Optional) Configure the `config.json` file within the Docker container to specify folder paths and settings according to your environment. You can use the default values or change them as needed.

### Setting Up the Cron Job

To schedule periodic execution of the project's `fullprocess.py` script, follow these steps:

1. Start the API service by running the `app.py` script in the working directory:

   ```bash
   python app.py
   ```

2. Inside the Docker container, set up the cron job using the command saved in `cronjob.txt`:

   ```bash
   crontab /home/jovyan/work/Dynamic_Risk_Assessment_System/cronjob.txt
   ```

   This will schedule the `fullprocess.py` script to run periodically, executing it every 10 minutes.