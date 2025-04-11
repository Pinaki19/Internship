import pandas as pd

# Load both files
trial_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\New\trial_results.csv")  # Contains: row_num, patient_id, visit_date, ...
notes_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\New\clinician_notes.csv")  # Contains: note_id, patient_id, region_id, note_date, ...

# date_columns = ['visit_date']  # <-- adjust these as needed

# # Convert and reformat dates
# for col in date_columns:
#     trial_df[col] = pd.to_datetime(trial_df[col], errors='coerce').dt.strftime('%d-%m-%Y')

# trial_df.to_csv(r"C:\Users\pinak\Downloads\Internship\New\trial_results.csv",index=False)
# Merge based on patient_id and matching dates
merged_df = pd.merge(
    notes_df,
    trial_df,
    how='inner',
    left_on=['patient_id', 'note_date'],
    right_on=['patient_id', 'visit_date']
)

# Optional: drop duplicate date columns (keeping only one)
merged_df.drop(columns=['note_id','note_date','region_id','row_num','health_metric','adverse_event'], inplace=True)

# Save the merged DataFrame
merged_df.to_csv(r"C:\Users\pinak\Downloads\Internship\New\merged_clinician_notes.csv", index=False)

#notes_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\New\merged_clinician_notes.csv")

# # Convert date columns to datetime format
# trial_df['visit_date'] = pd.to_datetime(trial_df['visit_date'], errors='coerce')
# notes_df['note_date'] = pd.to_datetime(notes_df['note_date'], errors='coerce')

# # Prepare a lookup from merged clinician notes (with non-null outcomes)
# notes_lookup = notes_df[['patient_id', 'note_date', 'trial_outcome']].dropna()

# # Merge to get updated trial_outcome using patient_id and matching visit_date ↔ note_date
# updated_trial_df = pd.merge(
#     trial_df,
#     notes_lookup,
#     how='left',
#     left_on=['patient_id', 'visit_date'],
#     right_on=['patient_id', 'note_date'],
#     suffixes=('', '_from_notes')
# )

# # Replace trial_outcome only if a non-null value exists in notes
# updated_trial_df['trial_outcome'] = updated_trial_df['trial_outcome_from_notes'].combine_first(updated_trial_df['trial_outcome'])

# # Drop helper columns
# updated_trial_df.drop(columns=['trial_outcome_from_notes', 'note_date'], inplace=True)

# # Save the corrected DataFrame
# updated_trial_df.to_csv(r"C:\Users\pinak\Downloads\Internship\New\corrected_trial_results.csv", index=False)


# # Load both files
# clean_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\New\new_results.csv")  # File with cleaned/updated trial_outcomes
# detailed_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\New\trial_results.csv")  # File to be corrected

# # Merge to get the correct trial_outcome from the clean file
# merged_df = pd.merge(
#     detailed_df,
#     clean_df[['patient_id', 'visit_date', 'trial_outcome']],
#     on=['patient_id', 'visit_date'],
#     how='left',
#     suffixes=('', '_corrected')
# )

# # Replace the trial_outcome in the detailed file with the corrected one if it exists
# merged_df['trial_outcome'] = merged_df['trial_outcome_corrected'].combine_first(merged_df['trial_outcome'])

# # Drop helper column
# merged_df.drop(columns=['trial_outcome_corrected'], inplace=True)

# # Save the updated file
# merged_df.to_csv(r"C:\Users\pinak\Downloads\Internship\New\corrected_trial_results_detailed.csv", index=False)
