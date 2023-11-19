import random
from datetime import datetime, timedelta
from faker import Faker

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
def generate_vitals(demographic_data):
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