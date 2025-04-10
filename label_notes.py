from textblob import TextBlob
import re
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return text

def get_medical_sentiment_textblob(text):
    text = preprocess_text(text)
    score = 0

    # Medical-specific positive indicators
    POSITIVE_INDICATORS = {
        'improved': 1.0, 'reduced': 0.8, 'decreased': 0.8, 'controlled': 0.6,
        'stable': 0.5, 'normal': 0.5, 'resolved': 1.0, 'healing': 0.8,
        'well-controlled': 0.9, 'gained': 0.7, 'concentrate': 0.6,
        'return to normal': 0.9, 'reduction': 0.7, 'noticeably reduced': 0.8,
        'significantly reduced': 0.9, 'climb stairs': 0.7,
        'healthy granulation': 0.8, 'sleeping through': 0.7
    }

    # Medical-specific negative indicators
    NEGATIVE_INDICATORS = {
        'worsened': -1.0, 'elevated': -0.7, 'increased pain': -0.8,
        'deteriorating': -0.9, 'declined': -0.8, 'infection': -0.7,
        'exacerbation': -0.8, 'adverse': -0.7, 'lost': -0.8,
        'unintentionally': -0.6, 'interfering': -0.7, 'purulent': -0.9,
        'erythema': -0.7, 'suicidal': -1.0, 'anhedonia': -0.8,
        'dyspnea': -0.8, 'nighttime awakening': -0.7, 'intensified': -0.8
    }

    # Check for medical-specific indicators
    for term, value in POSITIVE_INDICATORS.items():
        if term in text:
            score += value

    for term, value in NEGATIVE_INDICATORS.items():
        if term in text:
            score += value

    # Get TextBlob sentiment
    blob_score = TextBlob(text).sentiment.polarity

    # Use optimal weights found from grid search
    final_score = (score * 0.39) + (blob_score * 0.61)

    # Use optimal cutoffs found from grid search
    if final_score <= -0.14:
        return 'Negative'
    elif final_score >= 0.44:
        return 'Positive'
    return 'Neutral'




def get_medical_sentiment_vader(text):
    score = 0
    # Medical-specific positive indicators
    POSITIVE_INDICATORS = {
        'improved': 1.0, 'reduced': 0.8, 'decreased': 0.8, 'controlled': 0.6,
        'stable': 0.5, 'normal': 0.5, 'resolved': 1.0, 'healing': 0.8,
        'well-controlled': 0.9, 'gained': 0.7, 'concentrate': 0.6,
        'return to normal': 0.9, 'reduction': 0.7, 'noticeably reduced': 0.8,
        'significantly reduced': 0.9, 'climb stairs': 0.7,
        'healthy granulation': 0.8, 'sleeping through': 0.7
    }
    
    # Medical-specific negative indicators
    NEGATIVE_INDICATORS = {
        'worsened': -1.0, 'elevated': -0.7, 'increased pain': -0.8,
        'deteriorating': -0.9, 'declined': -0.8, 'infection': -0.7,
        'exacerbation': -0.8, 'adverse': -0.7, 'lost': -0.8,
        'unintentionally': -0.6, 'interfering': -0.7, 'purulent': -0.9,
        'erythema': -0.7, 'suicidal': -1.0, 'anhedonia': -0.8,
        'dyspnea': -0.8, 'nighttime awakening': -0.7, 'intensified': -0.8
    }
    
    # Check for medical-specific indicators
    for term, value in POSITIVE_INDICATORS.items():
        if term in text:
            score += value
            
    for term, value in NEGATIVE_INDICATORS.items():
        if term in text:
            score += value
    
    # Get VADER sentiment
    vader_score = sid.polarity_scores(text)['compound']
    
    # Use optimal weights found from grid search
    final_score = (score * 0.61) + (vader_score * 0.39)
    
    # Use optimal cutoffs found from grid search
    if final_score <= -0.35:
        return 'Negative'
    elif final_score >= 0.5:
        return 'Positive'
    return 'Neutral'


def main():
    # Textblob 
    # Read the data
    df = pd.read_csv('cleaned_notes.csv')

    # Apply sentiment analysis
    df['predicted_sentiment'] = df['note_text'].apply(get_medical_sentiment_textblob)

    # Save to new CSV
    df.to_csv('labeled_notes_textblob.csv', index=False)

    print("Notes have been labeled and saved to labeled_notes.csv")

    #Vader
    # Apply sentiment analysis
    df['predicted_sentiment'] = df['note_text'].apply(get_medical_sentiment_vader)

    # Save to new CSV
    df.to_csv('labeled_notes_vader.csv', index=False)

    print("Notes have been labeled using VADER and saved to vader_labeled_notes.csv")


if __name__=="__main__":
    main()