import pandas as pd
from datetime import datetime, timedelta
import random


def load_demographic_data(csv_file_path):
    # 从CSV文件读取数据
    df = pd.read_csv(csv_file_path)

    # 将DataFrame转换为字典列表
    return df.to_dict(orient='records')


def discharge_active_patients(demographic_data, discharge_percentage=10):
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
        patient['LOS'] = (current_date - admit_date).days + 1


def generate_vitals_record_for_discharge(demographic_data):
    vitals_data = []
    for patient in demographic_data:
        # 检查 discharge_date 是否为有效字符串
        if isinstance(patient['discharge_date'], str):
            discharge_date = datetime.strptime(patient['discharge_date'], '%Y-%m-%d').date()
            vitals_date = discharge_date - timedelta(days=1)

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
            vitals_record = {
                'patient_id': patient['patient_id'],
                'Date': vitals_date.strftime('%Y-%m-%d'),
                'Temperature': temperature,
                'Heart Rate': heart_rate,
                'Blood Pressure (Systolic)': systolic_bp,
                'Blood Pressure (Diastolic)': diastolic_bp,
                'Respiratory Rate': respiratory_rate,
                'O2 Saturation': o2_saturation,
                'Pain': pain,
                'Weight': weight,
                'Blood Glucose': blood_glucose,
            }
            vitals_data.append(vitals_record)

    return vitals_data


def generate_diagnosis_record_for_discharge(demographic_data):
    diagnosis_data = []
    diagnosis_codes = ["A00", "A01", "B00", "B01", "C00", "C01"]  # 示例ICD-10代码
    severities = ["Low", "Medium", "High"]

    for patient in demographic_data:
        # 检查 discharge_date 是否为有效字符串
        if isinstance(patient['discharge_date'], str):
            discharge_date = datetime.strptime(patient['discharge_date'], '%Y-%m-%d').date()
            diagnosis_date = discharge_date - timedelta(days=1)
            diagnosis_code = random.choice(diagnosis_codes)
            severity = random.choice(severities)
            # 生成诊断记录
            diagnosis_record = {
                'diagnosis_id': len(diagnosis_data) + 1,
                'patient_id': patient['patient_id'],
                'diagnosis_date': diagnosis_date.strftime('%Y-%m-%d'),
                "diagnosis_code": diagnosis_code,
                "diagnosis_description": f"Description for {diagnosis_code}",
                "severity": severity
            }
            diagnosis_data.append(diagnosis_record)

    return diagnosis_data


# 然后进行数据处理

# 读取现有的demographic数据
csv_file_path = 'C:/workspace/demographic_data_final.csv'
demographic_data = load_demographic_data(csv_file_path)

# 调用函数并传入出院比例参数
discharge_active_patients(demographic_data, discharge_percentage=10)

# 为即将出院的患者生成生命体征和诊断记录
vitals_data_for_discharge = generate_vitals_record_for_discharge(demographic_data)
diagnosis_data_for_discharge = generate_diagnosis_record_for_discharge(demographic_data)

# 保存更新后的数据
df_updated = pd.DataFrame(demographic_data)
vitals_df = pd.DataFrame(vitals_data_for_discharge)
diagnosis_df = pd.DataFrame(diagnosis_data_for_discharge)

# 将DataFrame保存为CSV文件
df_updated.to_csv('C:/workspace/updated_demographic_data.csv', index=False)
vitals_df.to_csv('C:/workspace/updated_vitals_data.csv', index=False)
diagnosis_df.to_csv('C:/workspace/updated_diagnosis_data.csv', index=False)
