
import pandas as pd

# Read the datasets
trial_df = pd.read_csv('trial_results.csv')
cleaned_notes_df = pd.read_csv('cleaned_notes.csv')
clinician_notes_df = pd.read_csv('clinician_notes.csv')
patients_df = pd.read_csv('patients_data.csv')

# Get note samples focused on stable and worsened outcomes
sample_visits = pd.concat([
    trial_df[trial_df['trial_outcome'] == 'Stable'].sample(n=6, random_state=42),
    trial_df[trial_df['trial_outcome'] == 'Worsened'].sample(n=6, random_state=42)
])

# Create new notes
new_notes = []
note_id_start = clinician_notes_df['note_id'].max() + 1

for _, row in sample_visits.iterrows():
    # Get matching note text for the outcome
    matching_note = cleaned_notes_df[
        cleaned_notes_df['trial_outcome'] == row['trial_outcome']
    ].sample(n=1).iloc[0]
    
    # Get region_id from patients_data.csv
    region_id = patients_df[patients_df['patient_id'] == row['patient_id']]['region_id'].iloc[0]
    
    new_notes.append({
        'note_id': note_id_start + len(new_notes),
        'patient_id': row['patient_id'],
        'region_id': region_id,
        'note_date': row['visit_date'],
        'note_text': matching_note['note_text']
    })

# Create DataFrame with new notes
new_notes_df = pd.DataFrame(new_notes)

# Append to existing clinician notes
updated_notes_df = pd.concat([clinician_notes_df, new_notes_df], ignore_index=True)

# Save updated dataset
updated_notes_df.to_csv('clinician_notes.csv', index=False)
print(f"Added {len(new_notes)} new notes (focused on stable and worsened outcomes) to clinician_notes.csv")
