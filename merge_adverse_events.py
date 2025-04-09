
import pandas as pd

# Read the CSV files
notes_df = pd.read_csv('clinician_notes.csv')
trials_df = pd.read_csv('trial_results.csv')

# Convert date columns to same format for comparison
notes_df['note_date'] = pd.to_datetime(notes_df['note_date'], format='%d-%m-%Y')
trials_df['visit_date'] = pd.to_datetime(trials_df['visit_date'], format='%d-%m-%Y')

# Merge the dataframes on patient_id and matching dates
merged_df = pd.merge(
    notes_df,
    trials_df[['patient_id', 'visit_date', 'adverse_event']],
    left_on=['patient_id', 'note_date'],
    right_on=['patient_id', 'visit_date'],
    how='left'
)

# Clean up the result
merged_df = merged_df.drop('visit_date', axis=1)  # Remove duplicate date column
merged_df['note_date'] = merged_df['note_date'].dt.strftime('%d-%m-%Y')  # Convert back to original format

# Save to new CSV file
merged_df.to_csv('notes_with_adverse_events.csv', index=False)
print("Created notes_with_adverse_events.csv with merged adverse event data")
