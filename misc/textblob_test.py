import pandas as pd
import numpy as np
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from sklearn.metrics import accuracy_score

# Ensure NLTK resources are downloaded
#nltk.download("all")
#nltk.download('punkt_tab')
# nltk.download('punkt', raise_on_error=True)
#nltk.download('wordnet', raise_on_error=True)
# nltk.download('omw-1.4', raise_on_error=True)

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

    # Tokenize and lemmatize
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join back to string
    return " ".join(lemmatized_tokens)

# ------------------ Load & Clean ------------------
df = pd.read_csv('notes_with_outcomes.csv')

# Keep only necessary columns, drop duplicates
df = df[['note_text', 'trial_outcome']].drop_duplicates()

# Compute polarity using TextBlob
def get_polarity(text):
    normalized_text=preprocess_text(text)
    return TextBlob(str(normalized_text)).sentiment.polarity


# df['polarity'] = df['note_text'].apply(get_polarity)

# # Map expected sentiment from trial outcome
# def expected_label(outcome):
#     outcome=outcome.lower()
#     if outcome== 'worsened':
#         return 'Negative'
#     elif outcome== "improved":
#         return "Positive"
#     else:
#         return 'Neutral'

# df['expected_sentiment'] = df['trial_outcome'].apply(expected_label)

# #------------------ Grid Search ------------------
# neg_cutoffs = np.linspace(-0.4, -0.05, 10)  # More negative = more strict
# pos_cutoffs = np.linspace(0.05, 0.4, 10)    # More positive = more strict

# results = []

# for neg in neg_cutoffs:
#     for pos in pos_cutoffs:
#         # Classify based on current cutoffs
#         def label_from_polarity(p):
#             if p >= pos:
#                 return 'Positive'
#             elif p <= neg:
#                 return 'Negative'
#             else:
#                 return 'Neutral'

#         df['predicted_sentiment'] = df['polarity'].apply(label_from_polarity)

#         # Evaluate match with expected sentiment
#         def is_correct(pred, expected):
#             if expected == 'Neutral':  
#                 return pred in ['Neutral', 'Positive']
#             return pred == expected

#         df['is_correct'] = df.apply(lambda row: is_correct(row['predicted_sentiment'], row['expected_sentiment']), axis=1)
#         adj_acc = df['is_correct'].mean()
#         true_acc = accuracy_score(df['expected_sentiment'], df['predicted_sentiment'])
        
#         results.append({
#             'neg_cutoff': neg,
#             'pos_cutoff': pos,
#             'true_accuracy': true_acc,
#             'adjusted_accuracy': adj_acc
#         })


# #------------------ Visualize ------------------
# results_df = pd.DataFrame(results)
#Pivot to make a heatmap
# pivot = results_df.pivot(index='neg_cutoff', columns='pos_cutoff', values='accuracy')

# plt.figure(figsize=(10, 8))
# sns.heatmap(pivot, annot=True, fmt=".2%", cmap="YlGnBu", cbar_kws={'label': 'Accuracy'})
# plt.title('Grid Search Accuracy for Sentiment Cutoffs')
# plt.xlabel('Positive Cutoff')
# plt.ylabel('Negative Cutoff')
# plt.tight_layout()
# plt.savefig("sentiment_cutoff_grid_heatmap.png")
# plt.show()

# # Print best configuration
# best = results_df.loc[results_df['true_accuracy'].idxmax()]
# print("\nBest Configuration:")
# print(best)
