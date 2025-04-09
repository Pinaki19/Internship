
import pandas as pd

# Read the CSV files
notes_df = pd.read_csv('clinician_notes.csv')
trials_df = pd.read_csv('trial_results.csv')

# Merge the dataframes on patient_id and visit_date
merged_df = pd.merge(
    notes_df,
    trials_df[['patient_id', 'visit_date', 'adverse_event']],
    on=['patient_id', 'visit_date'],
    how='left'
)

# Save to new CSV file
merged_df.to_csv('notes_with_adverse_events.csv', index=False)
print("Created notes_with_adverse_events.csv with merged adverse event data")
