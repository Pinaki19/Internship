import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged data
df = pd.read_csv(r"C:\Users\pinak\Downloads\Internship\combined_discrepancies.csv")

# Ensure boolean values are treated properly
df['adverse_event'] = df['adverse_event'].astype(bool)
df['adverse_effect'] = df['adverse_effect'].astype(bool)

# Discrepancy 1: Adverse event recorded, but no effect in note
event_no_effect = df[(df['adverse_event'] == True) & (df['adverse_effect'] == False)]

# Discrepancy 2: Adverse effect in note, but no event recorded
effect_no_event = df[(df['adverse_event'] == False) & (df['adverse_effect'] == True)]

# Combine both discrepancies into one DataFrame
discrepancies = pd.concat([event_no_effect, effect_no_event])

# Count discrepancies for each type
discrepancy_counts = discrepancies['discrepancy_type'].value_counts()

# Plotting the results
plt.figure(figsize=(8, 6))
sns.barplot(x=discrepancy_counts.index, y=discrepancy_counts.values, palette='Blues_d')

# Adding labels and title
plt.title("Discrepancies between Adverse Event and Adverse Effect")
plt.xlabel("Discrepancy Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')

# Show plot
plt.tight_layout()
plt.show()
