
import pandas as pd

# Read the CSV file
df = pd.read_csv('clinician_notes_with_outcomes.csv')

# Drop the trial_outcome column
df = df.drop('trial_outcome', axis=1)

# Save to new CSV file
df.to_csv('clinician_notes.csv', index=False)
print("Created clinician_notes.csv without trial_outcome column")
