from datetime import datetime, timedelta
from faker import Faker


# Generate demographic data with admission and discharge dates
# patient_id: Unique patient identifier

def generate_new_patients(num_records):
    demographic_data = []
    for patient_id in range(1, num_records + 1):
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
        # Generate a birth date for patients older than 50
        birth_date = fake.date_of_birth(minimum_age=50)
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
    return demographic_data


# update the active patient to discharge
def update_patient_status(demographic_data, discharge_percentage=10):
    # 当前日期
    current_date = datetime.now().date()

    # 筛选出活跃患者
    active_patients = [patient for patient in demographic_data if patient['Active_Stay_Ind'] == 1]

    # 计算需要出院的患者数量
    num_patients_to_discharge = int(len(active_patients) * discharge_percentage / 100)

    # 随机选择一定比例的患者进行出院处理
    patients_to_discharge = random.sample(active_patients, num_patients_to_discharge)

    for patient in patients_to_discharge:
        patient['discharge_date'] = current_date.strftime('%Y-%m-%d')
        patient['Active_Stay_Ind'] = 0
        admit_date = datetime.strptime(patient['admit_date'], '%Y-%m-%d').date()
