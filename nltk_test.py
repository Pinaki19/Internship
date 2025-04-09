import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Initialize VADER
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# ------------------ Load & Clean ------------------
df = pd.read_csv('cleaned_notes.csv')

# Remove duplicates and keep only needed fields
df = df[['note_text', 'trial_outcome']].drop_duplicates()

# Compute compound polarity score from VADER
df['polarity'] = df['note_text'].apply(lambda text: sid.polarity_scores(str(text))['compound'])

# Map expected sentiment
def expected_label(outcome):
    if outcome.lower() == 'worsened':
        return 'Negative'
    else:
        return 'Non-Negative'

df['expected_sentiment'] = df['trial_outcome'].apply(expected_label)

# ------------------ Grid Search ------------------
neg_cutoffs = np.linspace(-0.4, -0.05, 10)  # strict to lenient for negative
pos_cutoffs = np.linspace(0.05, 0.4, 10)    # lenient to strict for positive

results = []

for neg in neg_cutoffs:
    for pos in pos_cutoffs:
        # Label based on compound score
        def label(p):
            if p > pos:
                return 'Positive'
            elif p < neg:
                return 'Negative'
            else:
                return 'Neutral'

        df['predicted_sentiment'] = df['polarity'].apply(label)

        # Accuracy check
        def is_correct(pred, expected):
            if expected == 'Negative':
                return pred == 'Negative'
            else:
                return pred in ['Neutral', 'Positive']

        df['is_correct'] = df.apply(lambda row: is_correct(row['predicted_sentiment'], row['expected_sentiment']), axis=1)
        acc = df['is_correct'].mean()

        results.append({
            'neg_cutoff': neg,
            'pos_cutoff': pos,
            'accuracy': acc
        })

# ------------------ Save & Visualize ------------------
results_df = pd.DataFrame(results)
results_df.to_csv('vader_grid_search_results.csv', index=False)

# Heatmap
pivot = results_df.pivot(index='neg_cutoff', columns='pos_cutoff', values='accuracy')

plt.figure(figsize=(10, 8))
sns.heatmap(pivot, annot=True, fmt=".2%", cmap="coolwarm", cbar_kws={'label': 'Accuracy'})
plt.title('VADER Grid Search Accuracy for Sentiment Cutoffs')
plt.xlabel('Positive Cutoff')
plt.ylabel('Negative Cutoff')
plt.tight_layout()
plt.savefig("vader_sentiment_cutoff_heatmap.png")
plt.show()

# Best configuration
best = results_df.loc[results_df['accuracy'].idxmax()]
print("\nBest Cutoff Configuration (VADER):")
print(best)
