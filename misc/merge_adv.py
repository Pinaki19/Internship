import pandas as pd

# Load both CSVs
notes_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\main\results\adverse_effects_results.csv")  # contains note_id, patient_id, region_id, note_date, note_text, trial_outcome, sentiment, adverse_effect
visits_df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\main\CSV\trial_results.csv")  # contains patient_id, visit_date, health_metric, adverse_event, trial_outcome

# Convert date columns to datetime
notes_df['note_date'] = pd.to_datetime(notes_df['note_date'])
visits_df['visit_date'] = pd.to_datetime(visits_df['visit_date'])

# Merge on patient_id and where note_date == visit_date
merged_df = pd.merge(
    notes_df,
    visits_df,
    left_on=['patient_id', 'note_date'],
    right_on=['patient_id', 'visit_date'],
    how='inner'
)

# Select only desired columns
final_df = merged_df[['patient_id', 'visit_date', 'adverse_event', 'adverse_effect', 'sentiment', 'note_text']]

# Save the result
final_df.to_csv("merged_adverse_notes.csv", index=False)

import pandas as pd

# Load the merged data
df = pd.read_csv("merged_adverse_notes.csv")

# Ensure boolean values are treated properly
df['adverse_event'] = df['adverse_event'].astype(bool)
df['adverse_effect'] = df['adverse_effect'].astype(bool)

# Count frequencies
event_count = df['adverse_event'].sum()
effect_count = df['adverse_effect'].sum()

print(f"Total Adverse Events recorded: {event_count}")
print(f"Total Adverse Effects flagged in notes: {effect_count}\n")

# Discrepancy 1: Adverse event recorded, but no effect in note
event_no_effect = df[(df['adverse_event'] == True) & (df['adverse_effect'] == False)]
event_no_effect['discrepancy_type'] = 'Adverse Event recorded, no Adverse Effect flagged'

# Discrepancy 2: Adverse effect in note, but no event recorded
effect_no_event = df[(df['adverse_event'] == False) & (df['adverse_effect'] == True)]
effect_no_event['discrepancy_type'] = 'Adverse Effect flagged, no Adverse Event recorded'

# Combine both discrepancies into one DataFrame
discrepancies = pd.concat([event_no_effect, effect_no_event])

# Optionally: Sort by visit_date for better analysis
discrepancies = discrepancies.sort_values(by=['visit_date'])

# Print combined discrepancies
print(f"\nTotal discrepancies found: {len(discrepancies)}")
print(discrepancies[['patient_id', 'visit_date', 'note_text', 'discrepancy_type']].head())

# Save the combined discrepancies
discrepancies.to_csv("combined_discrepancies.csv", index=False)
