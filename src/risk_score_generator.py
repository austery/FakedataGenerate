import random
from datetime import datetime, timedelta
from faker import Faker
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
def generate_risk_scores(demographic_data):
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
