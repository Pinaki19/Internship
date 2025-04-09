
import pandas as pd

# Read the CSV files
clinician_notes = pd.read_csv('clinician_notes.csv')
trial_results = pd.read_csv('trial_results.csv')

# Get unique patient IDs from clinician notes
patient_ids = clinician_notes['patient_id'].unique()

# For each patient ID, get their visit dates
for patient_id in patient_ids:
    visits = trial_results[trial_results['patient_id'] == patient_id]['visit_date'].sort_values()
    print(f"\nPatient ID: {patient_id}")
    print("Visit dates:")
    for date in visits:
        print(f"- {date}")
