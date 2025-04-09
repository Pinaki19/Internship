
import pandas as pd

# Read the CSV files
clinician_notes = pd.read_csv('clinician_notes.csv')
trial_results = pd.read_csv('trial_results.csv')

# Convert date columns to datetime
clinician_notes['note_date'] = pd.to_datetime(clinician_notes['note_date'], format='%d-%m-%Y')
trial_results['visit_date'] = pd.to_datetime(trial_results['visit_date'], format='%d-%m-%Y')

# Merge the dataframes
merged_data = pd.merge(
    clinician_notes,
    trial_results[['patient_id', 'visit_date', 'health_metric', 'adverse_event', 'trial_outcome']],
    left_on=['patient_id', 'note_date'],
    right_on=['patient_id', 'visit_date'],
    how='inner'
)

# Clean up the merged data
merged_data = merged_data.drop('visit_date', axis=1)  # Remove duplicate date column
merged_data = merged_data.sort_values(['patient_id', 'note_date'])  # Sort by patient ID and date

# Save to new CSV file
merged_data.to_csv('patient_visits_merged.csv', index=False)
print("Merged data saved to patient_visits_merged.csv")
