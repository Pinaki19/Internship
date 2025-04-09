
import pandas as pd
import re

# Read the merged data
df = pd.read_csv('notes_with_adverse_events.csv')

# Define keywords that indicate adverse effects
adverse_keywords = [
    'adverse', 'worsened', 'deteriorat', 'decline', 'elevated', 'increased pain',
    'decreased', 'lost.*kg', 'infection', 'erythema', 'purulent', 'dyspnea',
    'suicidal', 'exacerbation', 'interfering', 'side effects', 'elevated'
]

# Create regex pattern
pattern = '|'.join(adverse_keywords)

# Find mentions of adverse effects in notes
df['adverse_mentioned'] = df['note_text'].str.contains(pattern, case=False, regex=True)

# Compare with actual adverse_event flag
discrepancies = df[df['adverse_mentioned'] != df['adverse_event']]

# Calculate statistics
total_notes = len(df)
total_adverse_flags = df['adverse_event'].sum()
total_adverse_mentions = df['adverse_mentioned'].sum()
discrepancy_count = len(discrepancies)

print("\nAdverse Event Analysis:")
print(f"Total notes: {total_notes}")
print(f"Notes with adverse_event flag: {total_adverse_flags}")
print(f"Notes with adverse effect mentions: {total_adverse_mentions}")
print(f"Number of discrepancies: {discrepancy_count}")

print("\nDetailed Discrepancy Analysis:")
print("\nNotes flagged as adverse but no adverse mentions in text:")
false_positives = discrepancies[discrepancies['adverse_event'] == True]
print(f"Count: {len(false_positives)}")

print("\nNotes with adverse mentions but not flagged:")
false_negatives = discrepancies[discrepancies['adverse_event'] == False]
print(f"Count: {len(false_negatives)}")

# Save discrepancies for review
discrepancies.to_csv('adverse_event_discrepancies.csv', index=False)
print("\nDetailed discrepancies saved to 'adverse_event_discrepancies.csv'")
