import logging
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


def main():
    logging.info("Daily operations started.")
    try:
        # Load existing data
        demographic_data_file_path = create_file_path('demographic_data')
        current_demographic_data = load_data(demographic_data_file_path)

        # Discharge some patients and generate new ones
        if not current_demographic_data.empty:
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

        else:
            logging.warning("DataFrame is empty or patient_id column does not exist.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    logging.info("Daily operations completed.")


if __name__ == "__main__":
    main()
