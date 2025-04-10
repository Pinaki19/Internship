
from textblob import TextBlob
import re

# Medical-specific positive indicators
POSITIVE_INDICATORS = {
    'improved': 1.0,
    'reduced': 0.8,
    'decreased': 0.8,
    'controlled': 0.6,
    'stable': 0.5,
    'normal': 0.5,
    'resolved': 1.0,
    'healing': 0.8,
    'well-controlled': 0.9,
    'gained': 0.7,
    'concentrate': 0.6,
    'return to normal': 0.9,
    'reduction': 0.7,
    'noticeably reduced': 0.8,
    'significantly reduced': 0.9,
    'climb stairs': 0.7,
    'healthy granulation': 0.8,
    'sleeping through': 0.7
}

# Medical-specific negative indicators  
NEGATIVE_INDICATORS = {
    'worsened': -1.0,
    'elevated': -0.7,
    'increased pain': -0.8,
    'deteriorating': -0.9,
    'declined': -0.8,
    'infection': -0.7,
    'exacerbation': -0.8,
    'adverse': -0.7,
    'lost': -0.8,
    'unintentionally': -0.6,
    'interfering': -0.7,
    'purulent': -0.9,
    'erythema': -0.7,
    'suicidal': -1.0,
    'anhedonia': -0.8,
    'dyspnea': -0.8,
    'nighttime awakening': -0.7,
    'intensified': -0.8
}

def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return text

def get_medical_sentiment(text):
    text = preprocess_text(text)
    score = 0
    
    # Check for medical-specific indicators
    for term, value in POSITIVE_INDICATORS.items():
        if term in text:
            score += value
            
    for term, value in NEGATIVE_INDICATORS.items():
        if term in text:
            score += value
    
    # Combine with TextBlob sentiment
    blob_score = TextBlob(text).sentiment.polarity
    
    # Weight medical terms more heavily
    final_score = (score * 0.7) + (blob_score * 0.3)
    
    # Classify based on final score
    if final_score <= -0.3:
        return 'Negative'
    elif final_score >= 0.3:
        return 'Positive'
    return 'Neutral'

if __name__ == "__main__":
    import pandas as pd
    
    # Load data
    df = pd.read_csv('cleaned_notes.csv')
    
    # Apply medical sentiment analysis
    df['predicted_sentiment'] = df['note_text'].apply(get_medical_sentiment)
    
    # Map trial outcomes to sentiment
    outcome_map = {
        'Worsened': 'Negative',
        'Improved': 'Positive',
        'Stable': 'Neutral'
    }
    df['expected_sentiment'] = df['trial_outcome'].map(outcome_map)
    
    # Calculate accuracy
    accuracy = (df['predicted_sentiment'] == df['expected_sentiment']).mean()
    print(f"Accuracy: {accuracy:.2%}")
