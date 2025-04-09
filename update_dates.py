
import pandas as pd

# Read the CSV files
clinician_notes = pd.read_csv('clinician_notes_with_outcomes.csv')
trial_results = pd.read_csv('trial_results.csv')

# Create a mapping dictionary for each patient_id and trial_outcome combination
date_mapping = {}
for _, row in trial_results.iterrows():
    key = (row['patient_id'], row['trial_outcome'])
    if key not in date_mapping:
        date_mapping[key] = row['visit_date']

# Update note_date using the mapping
def get_matching_date(row):
    key = (row['patient_id'], row['trial_outcome'])
    return date_mapping.get(key, row['note_date'])

clinician_notes['note_date'] = clinician_notes.apply(get_matching_date, axis=1)

# Save the updated data
clinician_notes.to_csv('clinician_notes_with_outcomes.csv', index=False)
print("Note dates updated successfully")
