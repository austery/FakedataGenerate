import glob
import logging
import os

from config import config
from demographic_generator import generate_new_demographic, discharge_demographic
from risk_score_generator import generate_risk_scores
from vitals_generator import generate_vitals
from diagnosis_generator import generate_diagnoses
from data_manager import load_data, save_data
import pandas as pd
import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)


def create_file_path(base_name):
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # Format: 'YYYYMMDD'
    return f"{config['data_directory']}/{base_name}_{current_date}.csv"


def find_latest_file(directory, pattern):
    """Find the latest file in the directory matching the given pattern."""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file


def main():
    logging.info("Daily operations started.")
    initial_data_created = False  # Flag to track if initial data was created
    try:
        data_directory = config['data_directory']
        latest_file_pattern = 'demographic_data_*.csv'
        latest_file_path = find_latest_file(data_directory, latest_file_pattern)

        if latest_file_path:
            # Load data from the latest file
            current_demographic_data = pd.read_csv(latest_file_path)
        else:
            # Handle the case where no file is found (e.g., create initial data)
            logging.info("No existing data file found. Generating initial data.")
            current_demographic_data = generate_new_demographic(1, 100)
            risk_scores_data = generate_risk_scores(current_demographic_data)

            save_data(current_demographic_data, create_file_path('demographic_data'))
            save_data(risk_scores_data, create_file_path('risk_scores_data'))

            initial_data_created = True

        # Perform daily operations only if initial data wasn't created just now
        if not initial_data_created and not current_demographic_data.empty:
            max_patient_id = current_demographic_data['patient_id'].max()
            update_demographic_data = discharge_demographic(current_demographic_data)
            new_demographic_data = generate_new_demographic(max_patient_id + 1, config['new_patients_count'])
            all_demographic_data = pd.concat([update_demographic_data, new_demographic_data], ignore_index=True)

            # Generate related data for new patients
            risk_scores_data = generate_risk_scores(new_demographic_data)
            # vitals_data = generate_vitals(new_demographic_data)
            # diagnoses_data = generate_diagnoses(new_demographic_data)

            # Save updated data
            save_data(all_demographic_data, create_file_path('demographic_data'))
            save_data(risk_scores_data, create_file_path('risk_scores_data'))
            # save_data(vitals_data, create_file_path('vitals_data'))
            # save_data(diagnoses_data, create_file_path('diagnoses_data'))

        elif initial_data_created:
            logging.info("Initial data created. Skipping discharge and new patient generation for today.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info("Daily operations completed.")


if __name__ == "__main__":
    main()
