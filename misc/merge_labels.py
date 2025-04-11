
import pandas as pd

# Read both CSV files
vader_df = pd.read_csv('nltk_normal_labeled_notes.csv')
textblob_df = pd.read_csv('textblob_normal_labeled_notes.csv')

# Merge based on note_text, renaming the sentiment columns
merged_df = pd.merge(
    vader_df[['note_text',"trial_outcome",'vader_sentiment']],
    textblob_df[['note_text', 'textblob_sentiment']],
    on='note_text',
    how='outer'
)

# Save the merged results
merged_df.to_csv('merged_sentiment_labels.csv', index=False)
print("Created merged_sentiment_labels.csv with both VADER and TextBlob labels")
