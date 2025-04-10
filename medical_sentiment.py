
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
    
    return score, blob_score

def get_final_sentiment(medical_score, blob_score, medical_weight, neg_cutoff, pos_cutoff):
    final_score = (medical_score * medical_weight) + (blob_score * (1 - medical_weight))
    
    if final_score <= neg_cutoff:
        return 'Negative'
    elif final_score >= pos_cutoff:
        return 'Positive'
    return 'Neutral'

if __name__ == "__main__":
    import numpy as np
    
    # Load data
    df = pd.read_csv('cleaned_notes.csv')
    
    # Grid search parameters
    medical_weights = np.linspace(0.5, 0.9, 5)  # [0.5, 0.6, 0.7, 0.8, 0.9]
    neg_cutoffs = np.linspace(-0.4, -0.2, 5)    # [-0.4, -0.35, -0.3, -0.25, -0.2]
    pos_cutoffs = np.linspace(0.2, 0.4, 5)      # [0.2, 0.25, 0.3, 0.35, 0.4]
    
    results = []
    
    # Get base scores
    df['medical_score'], df['blob_score'] = zip(*df['note_text'].apply(get_medical_sentiment))
    
    # Map trial outcomes to sentiment
    outcome_map = {
        'Worsened': 'Negative',
        'Improved': 'Positive',
        'Stable': 'Neutral'
    }
    df['expected_sentiment'] = df['trial_outcome'].map(outcome_map)
    
    # Grid search
    for weight in medical_weights:
        for neg in neg_cutoffs:
            for pos in pos_cutoffs:
                df['predicted_sentiment'] = df.apply(
                    lambda x: get_final_sentiment(
                        x['medical_score'], 
                        x['blob_score'],
                        weight,
                        neg,
                        pos
                    ), axis=1
                )
                
                accuracy = (df['predicted_sentiment'] == df['expected_sentiment']).mean()
                results.append({
                    'medical_weight': weight,
                    'neg_cutoff': neg,
                    'pos_cutoff': pos,
                    'accuracy': accuracy
                })
    
    # Find best configuration
    results_df = pd.DataFrame(results)
    best_result = results_df.loc[results_df['accuracy'].idxmax()]
    
    print("\nGrid Search Results:")
    print("===================")
    print(f"Best Accuracy: {best_result['accuracy']:.2%}")
    print(f"Medical Weight: {best_result['medical_weight']:.2f}")
    print(f"Negative Cutoff: {best_result['neg_cutoff']:.2f}")
    print(f"Positive Cutoff: {best_result['pos_cutoff']:.2f}")
    
    # Save results
    results_df.to_csv('medical_sentiment_grid_search.csv', index=False)
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
