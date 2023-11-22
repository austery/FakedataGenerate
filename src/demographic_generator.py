from datetime import datetime, timedelta
from faker import Faker
import random
import pandas as pd


# Generate demographic data with admission and discharge dates
# patient_id: Unique patient identifier

def generate_new_demographic(starting_patient_id: int = 1, num_records: int = 20) -> pd.DataFrame:
    fake = Faker()

    demographic_data = []
    for patient_id in range(starting_patient_id, starting_patient_id + num_records):
        # Basic patient demographic information
        first_name = fake.first_name()  # Patient's first name
        last_name = fake.last_name()  # Patient's last name
        fac_name = fake.company()  # Facility name
        adt_from_loc_name = fake.street_name()  # Admit from location
        dchg_to_loc_name = fake.street_name()  # Discharge to location
        payer = fake.random_element(elements=('Medicare', 'Medicaid', 'Private'))  # Payer information
        unit_desc = fake.word()  # Unit description
        room_desc = fake.random_number(digits=3)  # Room description
        bed_desc = fake.random_number(digits=2)  # Bed description

        # Admission and discharge dates
        admit_date = fake.date_between(start_date='-90d', end_date='today')  # Admission date
        active_stay_ind = random.randint(0, 1)  # Randomly setting active stay indicator as 0 or 1
        discharge_date = None if active_stay_ind == 1 else fake.date_between(start_date=admit_date,
                                                                             end_date='today')  # Discharge date

        functional_independence = fake.random_element(
            elements=('Independent', 'Assistance Required', 'Dependent'))  # Level of functional independence
        # Generate a birthdate for patients older than 50
        birth_date = fake.date_of_birth(minimum_age=60)
        record = {
            'patient_id': patient_id,  # Unique patient identifier
            'first_name': first_name,
            'last_name': last_name,
            'fac_name': fac_name,
            'adt_from_loc_name': adt_from_loc_name,
            'dchg_to_loc_name': dchg_to_loc_name,
            'Payer': payer,
            'unit_desc': unit_desc,
            'room_desc': room_desc,
            'bed_desc': bed_desc,
            'admit_date': admit_date.strftime('%Y-%m-%d'),
            'discharge_date': '' if discharge_date is None else discharge_date.strftime('%Y-%m-%d'),
            'Active_Stay_Ind': active_stay_ind,  # Active stay indicator
            'Functional_Independence': functional_independence,
            'birth_date': birth_date.strftime('%Y-%m-%d')  # Birth date
        }
        demographic_data.append(record)
    return pd.DataFrame(demographic_data)


# update the active patient to discharge
def discharge_demographic(demographic_data: pd.DataFrame, discharge_percentage: int = 10) -> pd.DataFrame:
    # Current date
    current_date = datetime.now().date()

    # Filter active patients
    active_patients = demographic_data[demographic_data['Active_Stay_Ind'] == 1]

    # Calculate the number of patients to discharge
    num_patients_to_discharge = int(len(active_patients) * discharge_percentage / 100)

    # Randomly select a certain percentage of patients for discharge
    patients_to_discharge_indices = random.sample(list(active_patients.index),
                                                  min(num_patients_to_discharge, len(active_patients)))

    # Update discharge date and active stay indicator
    for index in patients_to_discharge_indices:
        demographic_data.at[index, 'discharge_date'] = current_date.strftime('%Y-%m-%d')
        demographic_data.at[index, 'Active_Stay_Ind'] = 0

    return demographic_data
