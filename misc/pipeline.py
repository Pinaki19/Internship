import pandas as pd
from transformers import pipeline
from sklearn.metrics import classification_report, accuracy_score

# Load cleaned notes
df = pd.read_csv(r'C:\Users\pinak\Downloads\Internship\main\results\notes_with_outcomes.csv')

# Drop duplicates and nulls
df = df[['note_text', 'trial_outcome']].drop_duplicates().dropna()

# Expected sentiment mapping
def map_outcome(outcome):
    outcome = outcome.strip().lower()
    if outcome == 'worsened':
        return 'Negative'
    elif outcome == 'improved':
        return 'Positive'
    elif outcome == 'stable':
        return 'Neutral'  # Can be Positive or Neutral
    return None

df['expected'] = df['trial_outcome'].apply(map_outcome)
df = df[df['expected'].notna()]

# Hugging Face sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Predict sentiment
def get_sentiment(text):
    result = sentiment_pipeline(str(text))[0]
    label = result['label']
    if label == 'POSITIVE':
        return 'Positive'
    elif label == 'NEGATIVE':
        return 'Negative'
    else:
        return 'Neutral'

print("Analyzing sentiment...")
df['predicted'] = df['note_text'].apply(get_sentiment)

# Adjust for 'Stable' being either Neutral or Positive
def is_correct(pred, expected):
    if expected == 'Neutral':  # meaning 'Stable'
        return pred in ['Neutral', 'Positive']
    return pred == expected

df['correct'] = df.apply(lambda row: is_correct(row['predicted'], row['expected']), axis=1)
# Strict accuracy (true accuracy)
true_accuracy = accuracy_score(df['expected'], df['predicted'])

# Adjusted accuracy (flexible for 'Neutral' == 'Positive' or 'Neutral')
adjusted_accuracy = df['correct'].mean()

# Classification Report
report = classification_report(df['expected'], df['predicted'], digits=3)

# Output
# distilbert-base-uncased-finetuned-sst-2-english
print("\nClassification Report: Pipeline(DistilBERT)")
print(report)
print(f"True Accuracy: {true_accuracy:.4f} | Adjusted Accuracy: {adjusted_accuracy:.4f}")
