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
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Ensure NLTK resources are downloaded
# nltk.download("punkt")
# nltk.download('wordnet')
# nltk.download('omw-1.4')

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
df = pd.read_csv(r'C:\Users\pinak\Downloads\Internship\main\results\notes_with_outcomes.csv')

# Keep only necessary columns, drop duplicates
df = df[['note_text', 'trial_outcome']].drop_duplicates()

# Compute polarity using TextBlob
def get_polarity(text):
    normalized_text = preprocess_text(text)
    return TextBlob(str(normalized_text)).sentiment.polarity

df['polarity'] = df['note_text'].apply(get_polarity)

# Map expected sentiment from trial outcome
def expected_label(outcome):
    outcome = outcome.lower()
    if outcome == 'worsened':
        return 'Negative'
    elif outcome == "improved":
        return "Positive"
    else:
        return 'Neutral'

df['expected_sentiment'] = df['trial_outcome'].apply(expected_label)

# ------------------ Grid Search ------------------
neg_cutoffs = np.linspace(-0.4, -0.05, 10)  # More negative = more strict
pos_cutoffs = np.linspace(0.05, 0.4, 10)    # More positive = more strict

results = []

for neg in neg_cutoffs:
    for pos in pos_cutoffs:
        # Classify based on current cutoffs
        def label_from_polarity(p):
            if p >= pos:
                return 'Positive'
            elif p <= neg:
                return 'Negative'
            else:
                return 'Neutral'

        df['predicted_sentiment'] = df['polarity'].apply(label_from_polarity)

        # Evaluate match with expected sentiment
        def is_correct(pred, expected):
            if expected == 'Neutral':  
                return pred in ['Neutral', 'Positive']
            return pred == expected

        df['is_correct'] = df.apply(lambda row: is_correct(row['predicted_sentiment'], row['expected_sentiment']), axis=1)
        adj_acc = df['is_correct'].mean()
        true_acc = accuracy_score(df['expected_sentiment'], df['predicted_sentiment'])
        
        # Precision, Recall, and F1 Score
        precision = precision_score(df['expected_sentiment'], df['predicted_sentiment'], average='weighted', labels=['Positive', 'Neutral', 'Negative'])
        recall = recall_score(df['expected_sentiment'], df['predicted_sentiment'], average='weighted', labels=['Positive', 'Neutral', 'Negative'])
        f1 = f1_score(df['expected_sentiment'], df['predicted_sentiment'], average='weighted', labels=['Positive', 'Neutral', 'Negative'])

        results.append({
            'neg_cutoff': neg,
            'pos_cutoff': pos,
            'true_accuracy': true_acc,
            'adjusted_accuracy': adj_acc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        })

# ------------------ Save & Visualize ------------------
results_df = pd.DataFrame(results)

# Best configuration based on true_accuracy
best = results_df.loc[results_df['true_accuracy'].idxmax()]
print("\nBest Cutoff Configuration (TextBlob):")
print(best)

