import pandas as pd



def load_data(file_path):
    """Loads patient data from a CSV file."""
    return pd.read_csv(file_path)

def save_data(data, file_path):
    """Saves patient data to a CSV file."""
    data.to_csv(file_path, index=False)

def update_patient_status(patients):
    """Updates the status of patients (e.g., discharging patients)."""
    # Implement logic to update patient data
    return updated_patients