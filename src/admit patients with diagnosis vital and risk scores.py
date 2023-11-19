import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import json
import os

fake = Faker()


# Generate demographic data with admission and discharge dates
# patient_id: Unique patient identifier
# first_name: Patient's first name
# last_name: Patient's last name
# fac_name: Facility name
# adt_from_loc_name: Admit from location
# dchg_to_loc_name: Discharge to location
# Payer: Payer information
# unit_desc: Unit description
# room_desc: Room description
# bed_desc: Bed description
# admit_date: Admission date
# discharge_date: Discharge date
# Active_Stay_Ind: Active stay indicator as 0 or 1
# Functional_Independence: Functional independence level
def generate_demographic_data_final(num_records):
    demographic_data = []
    for patient_id in range(1, num_records + 1):
        # Generate a birth date for patients older than 50
        birth_date = fake.date_of_birth(minimum_age=50)

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
        admit_date = fake.date_between(start_date='-1y', end_date='today')  # Admission date
        active_stay_ind = random.randint(0, 1)  # Randomly setting active stay indicator as 0 or 1
        discharge_date = None if active_stay_ind == 1 else fake.date_between(start_date=admit_date,
                                                                             end_date='today')  # Discharge date

        functional_independence = fake.random_element(
            elements=('Independent', 'Assistance Required', 'Dependent'))  # Level of functional independence

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


# Generate risk score records based on demographic data
# generate 30 risk score records for each patient if the stay duration is greater than 30 days
# otherwise, generate 1 risk score record for each day of the stay

# patient_id: Unique patient identifier
# ard_planner_id: Unique ID for each ARD entry
# ard: Assessment Reference Date
# target_date_type: Target date type
# rug_score: RUG score
# cmi: Case mix index
# minutes_from_higher_therapy: Minutes from higher therapy
# minutes_from_lower_therapy: Minutes from lower therapy
# points_from_higher_adl: Points from higher ADL
# created_by: Created by
# created_date: Created date
# revision_by: Revision by
# revision_date: Revision date
# total_minutes: Total minutes
# state_rug_score: State RUG score
# state_cmi: State case mix index#
def generate_risk_score_based_on_demographic(demographic_data):
    risk_score_data = []
    for patient in demographic_data:
        # Convert admit_date to date object and add 1 day
        admit_date = datetime.strptime(patient['admit_date'], '%Y-%m-%d').date() + timedelta(days=1)
        # If Active_Stay_Ind is 1, use the current date minus one day as the end date
        if patient['Active_Stay_Ind'] == 1:
            end_date = datetime.now().date() - timedelta(days=1)
        else:  # Otherwise, use the discharge_date from demographic_data
            end_date = datetime.strptime(patient['discharge_date'], '%Y-%m-%d').date()

        # If the stay duration is more than 30 days, use the last 30 days
        if (end_date - admit_date).days > 30:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = admit_date

        # Generate a list of dates from start_date to end_date
        date_sequence = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        for i, record_date in enumerate(date_sequence):
            # Generate other risk score data fields
            rug_score = fake.random_element(elements=('RUG-IV', 'PDPM'))
            cmi = round(random.uniform(0.5, 1.5), 2)
            minutes_from_higher_therapy = random.randint(0, 500)
            minutes_from_lower_therapy = random.randint(0, 500)
            points_from_higher_adl = random.randint(0, 28)
            total_minutes = minutes_from_higher_therapy + minutes_from_lower_therapy
            state_rug_score = fake.random_element(elements=('A', 'B', 'C', 'D'))
            state_cmi = round(random.uniform(0.5, 1.5), 2)

            # Append a new risk score record to the list
            risk_score_data.append({
                'patient_id': patient['patient_id'],
                'ard_planner_id': patient['patient_id'] * 1000 + i,  # Unique ID for each ARD entry
                'ard': record_date.strftime('%Y-%m-%d'),  # Assessment Reference Date
                'target_date_type': fake.random_element(elements=('Admission', 'Quarterly', 'Annual')),
                'rug_score': rug_score,
                'cmi': cmi,
                'minutes_from_higher_therapy': minutes_from_higher_therapy,
                'minutes_from_lower_therapy': minutes_from_lower_therapy,
                'points_from_higher_adl': points_from_higher_adl,
                'created_by': fake.name(),
                'created_date': record_date.strftime('%Y-%m-%d'),
                'revision_by': fake.name(),
                'revision_date': record_date.strftime('%Y-%m-%d'),
                'total_minutes': total_minutes,
                'state_rug_score': state_rug_score,
                'state_cmi': state_cmi,
            })
    return risk_score_data


# Generate vitals data records based on demographic data
# generate 1 - 4 vitals records for each patient

# patient_id: Unique patient identifier
# Date: Date of the vital signs measurement
# Temperature: Body temperature
# Heart Rate: Heart rate
# Blood Pressure (Systolic): Systolic blood pressure
# Blood Pressure (Diastolic): Diastolic blood pressure
# Respiratory Rate: Respiratory rate
# O2 Saturation: Oxygen saturation
# Pain: Pain level
# Weight: Weight
# Blood Glucose: Blood glucose level
def generate_vitals_data_based_on_demographic(demographic_data):
    vitals_data = []
    for patient in demographic_data:
        num_vitals_records = random.randint(1, 4)
        for _ in range(num_vitals_records):
            admit_date = datetime.strptime(patient['admit_date'], '%Y-%m-%d')
            discharge_date = datetime.strptime(patient['discharge_date'], '%Y-%m-%d') if patient[
                'discharge_date'] else datetime.now().date()
            record_date = fake.date_between(start_date=admit_date, end_date=discharge_date)

            # Vital signs measurements
            temperature = round(random.uniform(96, 101), 1)  # Body temperature
            heart_rate = random.randint(60, 100)  # Heart rate
            systolic_bp = random.randint(90, 140)  # Systolic blood pressure
            diastolic_bp = random.randint(60, 90)  # Diastolic blood pressure
            respiratory_rate = random.randint(12, 20)  # Respiratory rate
            o2_saturation = random.randint(95, 100)  # Oxygen saturation
            pain = random.randint(0, 10)  # Pain level
            weight = round(random.uniform(100, 250), 1)  # Weight
            blood_glucose = random.randint(70, 200)  # Blood glucose level

            vitals_data.append({
                'patient_id': patient['patient_id'],
                'Date': record_date.strftime('%Y-%m-%d'),
                'Temperature': temperature,
                'Heart Rate': heart_rate,
                'Blood Pressure (Systolic)': systolic_bp,
                'Blood Pressure (Diastolic)': diastolic_bp,
                'Respiratory Rate': respiratory_rate,
                'O2 Saturation': o2_saturation,
                'Pain': pain,
                'Weight': weight,
                'Blood Glucose': blood_glucose,
            })
    return vitals_data


# Generate diagnosis data records based on demographic data
# generate 1 - 5 diagnosis records for each patient
def generate_diagnosis_data_based_on_demographic(demographic_data):
    diagnosis_data = []
    diagnosis_codes = ["A00", "A01", "B00", "B01", "C00", "C01"]  # 示例ICD-10代码
    severities = ["Low", "Medium", "High"]

    for patient in demographic_data:
        patient_id = patient["patient_id"]
        admit_date = datetime.strptime(patient["admit_date"], '%Y-%m-%d').date()
        discharge_date = datetime.now().date() if patient["Active_Stay_Ind"] == 1 else datetime.strptime(
            patient["discharge_date"], '%Y-%m-%d').date()

        # 为每位患者随机生成1到5条诊断记录
        num_diagnosis_records = random.randint(1, 5)
        for _ in range(num_diagnosis_records):
            diagnosis_date = fake.date_between(start_date=admit_date, end_date=discharge_date)
            diagnosis_code = random.choice(diagnosis_codes)
            severity = random.choice(severities)

            diagnosis_data.append({
                "diagnosis_id": len(diagnosis_data) + 1,
                "patient_id": patient_id,
                "diagnosis_code": diagnosis_code,
                "diagnosis_description": f"Description for {diagnosis_code}",
                "diagnosis_date": diagnosis_date.strftime('%Y-%m-%d'),
                "severity": severity
            })

    return diagnosis_data


# Set the number of records to generate
num_records = 150

# Generate final demographic data
demographic_data_final = generate_demographic_data_final(num_records)

# Generate final risk score and vitals data based on demographic data
risk_score_data_final = generate_risk_score_based_on_demographic(demographic_data_final)
vitals_data_final = generate_vitals_data_based_on_demographic(demographic_data_final)
diagnosis_data_final = generate_diagnosis_data_based_on_demographic(demographic_data_final)

# Save the final demographic data to a CSV file
demographic_path_final = 'c:/workspace/demographic_data_final.csv'
with open(demographic_path_final, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=demographic_data_final[0].keys())
    writer.writeheader()
    writer.writerows(demographic_data_final)

# Save the final risk score data to a CSV file, ensuring unique ARD planner IDs and sorted ARD dates
risk_score_path_final = 'c:/workspace/risk_score_data_final.csv'
with open(risk_score_path_final, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=risk_score_data_final[0].keys())
    writer.writeheader()
    writer.writerows(risk_score_data_final)

# Save the final vitals data to a CSV file
vitals_path_final = 'c:/workspace/vitals_data_final.csv'
with open(vitals_path_final, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=vitals_data_final[0].keys())
    writer.writeheader()
    writer.writerows(vitals_data_final)

# Save the final diagnosis data to a CSV file
diagnosis_path_final = 'c:/workspace/diagnosis_data_final.csv'
with open(diagnosis_path_final, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=diagnosis_data_final[0].keys())
    writer.writeheader()
    writer.writerows(diagnosis_data_final)


def save_patient_data_as_json(patient_id, demographic_data, risk_score_data, vitals_data, diagnosis_data, directory):
    # 确保目录存在，如果不存在，则创建它
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 创建包含所有相关数据的字典
    patient_data = {
        "demographic_data": [data for data in demographic_data if data["patient_id"] == patient_id],
        "risk_score_data": [data for data in risk_score_data if data["patient_id"] == patient_id],
        "vitals_data": [data for data in vitals_data if data["patient_id"] == patient_id],
        "diagnosis_data": [data for data in diagnosis_data if data["patient_id"] == patient_id]
    }

    # 构建完整的文件路径
    file_path = os.path.join(directory, f'patient_{patient_id}_data.json')

    # 将数据保存为JSON文件
    with open(file_path, 'w') as file:
        json.dump(patient_data, file, indent=4)


# 指定保存文件的目录
directory = 'c:/workspace/first50'

# 示例：为每位患者生成JSON文件
for patient_id in range(1, num_records + 1):
    save_patient_data_as_json(patient_id, demographic_data_final, risk_score_data_final, vitals_data_final,
                              diagnosis_data_final, directory)


def generate_vitals_record_for_discharge(demographic_data):
    vitals_data = []
    for patient in demographic_data:
        if patient['discharge_date']:
            discharge_date = datetime.strptime(patient['discharge_date'], '%Y-%m-%d').date()
            vitals_date = discharge_date - timedelta(days=1)

            # 生成生命体征记录
            vitals_record = {
                'patient_id': patient['patient_id'],
                'Date': vitals_date.strftime('%Y-%m-%d'),
                # 添加其它生命体征数据...
            }
            vitals_data.append(vitals_record)

    return vitals_data
