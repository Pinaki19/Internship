
import pandas as pd

# Read the CSV file
df = pd.read_csv('trial_results.csv')

# Sort by patient_id
df_sorted = df.sort_values('patient_id')

# Save back to the same file
df_sorted.to_csv('trial_results.csv', index=False)
print("Trial results sorted by patient_id")
