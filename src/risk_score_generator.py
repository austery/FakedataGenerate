import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd


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
def generate_risk_scores(demographic_df: pd.DataFrame) -> pd.DataFrame:
    fake = Faker()
    risk_score_records = []

    for index, patient in demographic_df.iterrows():
        # Convert admit_date to a datetime.date object
        admit_date = pd.to_datetime(patient['admit_date']).date() + timedelta(days=1)

        # Ensure end_date is also a datetime.date object
        if patient['Active_Stay_Ind'] == 1:
            end_date = datetime.now().date() - timedelta(days=1)
        else:
            # Convert discharge_date to a datetime.date object
            end_date = pd.to_datetime(patient['discharge_date']).date()

        # Now both dates are datetime.date objects and can be subtracted
        if (end_date - admit_date).days > 30:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = admit_date

        date_sequence = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        for i, record_date in enumerate(date_sequence):
            rug_score = fake.random_element(elements=('RUG-IV', 'PDPM'))
            cmi = round(random.uniform(0.5, 1.5), 2)
            minutes_from_higher_therapy = random.randint(0, 500)
            minutes_from_lower_therapy = random.randint(0, 500)
            points_from_higher_adl = random.randint(0, 28)
            total_minutes = minutes_from_higher_therapy + minutes_from_lower_therapy
            state_rug_score = fake.random_element(elements=('A', 'B', 'C', 'D'))
            state_cmi = round(random.uniform(0.5, 1.5), 2)

            risk_score_record = {
                'patient_id': patient['patient_id'],
                'ard_planner_id': patient['patient_id'] * 1000 + i,
                'ard': record_date.strftime('%Y-%m-%d'),
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
            }
            risk_score_records.append(risk_score_record)

    return pd.DataFrame(risk_score_records)
