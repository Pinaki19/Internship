
import pandas as pd

# Read the merged labels file
df = pd.read_csv('merged_sentiment_labels.csv')

# Find rows where VADER and TextBlob labels differ
discrepancies = df[df['vader_label'] != df['textblob_label']]

# Save to new CSV
discrepancies.to_csv('sentiment_label_discrepancies.csv', index=False)

print(f"Found {len(discrepancies)} discrepancies between VADER and TextBlob labels")
print("Saved discrepancies to sentiment_label_discrepancies.csv")
