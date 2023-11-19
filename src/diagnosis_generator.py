import random
from datetime import datetime, timedelta
from faker import Faker

# Generate diagnosis data records based on demographic data
# generate 1 - 5 diagnosis records for each patient
def generate_diagnoses(demographic_data):
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