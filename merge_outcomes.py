
import pandas as pd

# Read the CSV files
clinician_notes = pd.read_csv('clinician_notes.csv')
cleaned_notes = pd.read_csv('cleaned_notes.csv')

# Merge based on note text
merged_data = pd.merge(clinician_notes, 
                      cleaned_notes[['note_text', 'trial_outcome']], 
                      on='note_text', 
                      how='left')

# Save to new CSV file
merged_data.to_csv('clinician_notes_with_outcomes.csv', index=False)
print("Merged data saved to clinician_notes_with_outcomes.csv")
