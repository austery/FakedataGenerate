import patient_generator
from risk_score_generator import generate_risk_scores
from vitals_generator import generate_vitals
from diagnosis_generator import generate_diagnoses
from data_manager import load_data, save_data, update_patient_status

def run_daily_operations():
    # Load existing data
    file_path = 'c:/workspace/demographic_data_final.csv'
    patient_data = load_data(file_path)

    # Update 10% patient statuses to discharge
    update_patient_status(patient_data)

    # Generate new patients
    new_patients = generate_new_patients(20)

    # Combine new and existing patients
    all_patients = patient_data + new_patients

    # Generate risk scores, vitals, and diagnoses for patients
    risk_scores = generate_risk_scores(all_patients)
    vitals = generate_vitals(all_patients)
    diagnoses = generate_diagnoses(all_patients)

    # Save updated data
    save_data(all_patients, risk_scores, vitals, diagnoses)

if __name__ == "__main__":
    run_daily_operations()
