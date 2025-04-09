
import pandas as pd

# Read the CSV files
clinician_notes = pd.read_csv('clinician_notes_with_outcomes.csv')
trial_results = pd.read_csv('trial_results.csv')

# Create a mapping dictionary for each unique combination
date_mapping = {}
used_dates = set()

# Sort trial results by visit_date to maintain chronological order
trial_results = trial_results.sort_values('visit_date')

for _, note_row in clinician_notes.iterrows():
    patient_id = note_row['patient_id']
    trial_outcome = note_row['trial_outcome']
    note_text = note_row['note_text']
    
    # Create key for the current note
    key = (patient_id, trial_outcome, note_text)
    
    if key not in date_mapping:
        # Find matching trial results
        matching_visits = trial_results[
            (trial_results['patient_id'] == patient_id) & 
            (trial_results['trial_outcome'] == trial_outcome)
        ]['visit_date']
        
        # Find first unused date
        for date in matching_visits:
            if date not in used_dates:
                date_mapping[key] = date
                used_dates.add(date)
                break

# Update note_date using the mapping
def get_matching_date(row):
    key = (row['patient_id'], row['trial_outcome'], row['note_text'])
    return date_mapping.get(key, row['note_date'])

clinician_notes['note_date'] = clinician_notes.apply(get_matching_date, axis=1)

# Save the updated data
clinician_notes.to_csv('clinician_notes_with_outcomes.csv', index=False)
print("Note dates updated successfully")
