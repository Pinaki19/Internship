
import pandas as pd

# Read both CSV files
vader_df = pd.read_csv('labeled_notes_vader.csv')
textblob_df = pd.read_csv('labeled_notes_textblob.csv')

# Merge based on note_text, renaming the sentiment columns
merged_df = pd.merge(
    vader_df[['note_text',"trial_outcome",'predicted_sentiment']].rename(columns={'predicted_sentiment': 'vader_label'}),
    textblob_df[['note_text', 'predicted_sentiment']].rename(columns={'predicted_sentiment': 'textblob_label'}),
    on='note_text',
    how='outer'
)

# Save the merged results
merged_df.to_csv('merged_sentiment_labels.csv', index=False)
print("Created merged_sentiment_labels.csv with both VADER and TextBlob labels")
