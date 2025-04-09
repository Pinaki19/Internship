from textblob import TextBlob
from collections import Counter
import re
from nltk.corpus import stopwords
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# Load the clinical notes
data = pd.read_csv('clinician_notes.csv')

# Download required NLTK data
#nltk.download('vader_lexicon')
#nltk.download('stopwords')

#Question 2
def count_notes_per_region():

    # Read the CSV files
    notes_df = pd.read_csv('clinician_notes.csv')
    regions_df = pd.read_csv('regions_data.csv')

    # Count notes per region
    notes_per_region = notes_df.groupby('region_id').size().reset_index(name='note_count')

    # Merge with region names
    result = pd.merge(
        notes_per_region,
        regions_df[['region_id', 'region_name']],
        on='region_id',
        how='left'
    )

    # Sort by region name
    result = result.sort_values('region_name')

    # Save results
    result.to_csv('notes_per_region.csv', index=False)

    # Print results
    print("\nNotes per Region:")
    print("================")
    for _, row in result.iterrows():
        print(f"{row['region_name']} (ID: {row['region_id']}): {row['note_count']} notes")

#Question 3
def report_top_words(n:int):
    def get_keywords(text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        stop_words = set(stopwords.words('english'))
        keywords = [word for word in words if word not in stop_words]
        return keywords

    all_keywords = []
    for note in data['note_text']:
        all_keywords.extend(get_keywords(note))

    keyword_counts = Counter(all_keywords)
    print(f"\nTop {n} most common keywords in clinical notes:")
    for word, count in keyword_counts.most_common(n):
        print(f"{word}: {count} occurrences")



#Question 4

def get_polarity(text):
    return TextBlob(str(text)).sentiment.polarity
    
Neg_cutoff=-0.24444
Pos_cutoff=0.050
def get_sentiment(text):
    polarity = get_polarity(text)
    if polarity <= Neg_cutoff:
        return 'Negative'
    elif polarity >= Pos_cutoff:
        return 'Positive'
    else:
        return 'Neutral'

def analyze_sentiment():
    #Perform sentiment analysis
    data['sentiment'] = data['note_text'].apply(get_sentiment)

    # Save results to CSV
    output_file = 'sentiment_analysis_results.csv'
    data.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")



def extract_numerical_changes(text):
    # Extract numerical changes using regex
    changes = re.findall(r'(\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?%|\d+(?:\.\d+)?)\s*(?:to|->)\s*(\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?%|\d+(?:\.\d+)?)', text)
    return changes

def analyze_negative_trends():
    # Read the sentiment analysis results
    df = pd.read_csv('sentiment_analysis_results.csv')

    # Filter for negative sentiment
    negative_notes = df[df['sentiment'] == 'Negative']

    # Initialize categories for trends
    trends = {
        'Physical Symptoms': [],
        'Mental Health': [],
        'Vital Signs': [],
        'Treatment Response': []
    }

    # Analyze each negative note
    for note in negative_notes['note_text']:
        # Physical Symptoms
        if any(term in note.lower() for term in ['pain', 'edema', 'tremor', 'dyspnea', 'wound']):
            trends['Physical Symptoms'].append(note)

        # Mental Health
        if any(term in note.lower() for term in ['anxiety', 'depression', 'cognitive', 'mood']):
            trends['Mental Health'].append(note)

        # Vital Signs
        if any(term in note.lower() for term in ['blood pressure', 'heart rate', 'oxygen', 'temperature']):
            trends['Vital Signs'].append(note)

        # Treatment Response
        if any(term in note.lower() for term in ['medication', 'treatment', 'therapy', 'dose']):
            trends['Treatment Response'].append(note)

    # Print summary
    print("\nNegative Trends Analysis Summary:")
    print("=================================")

    for category, instances in trends.items():
        if instances:
            print(f"\n{category}:")
            print("-" * len(category))
            for note in instances:
                # Extract and display numerical changes if present
                changes = extract_numerical_changes(note)
                if changes:
                    print(f"- {note.split('.')[0]} (Changes: {', '.join([f'{c[0]} to {c[1]}' for c in changes])})")
                else:
                    print(f"- {note.split('.')[0]}")


#Question 5 Wordcloud
def generate_wordcloud():
    df = pd.read_csv('clinician_notes.csv')
    # Combine all notes into one text
    text = ' '.join(df['note_text'].astype(str))
    # Get stopwords and add custom medical/common words to filter out
    stop_words = set(stopwords.words('english'))
    custom_stops = {'patient', 'reports', 'noted', 'unchanged', 'approximately', 'current', 'showing'}
    stop_words.update(custom_stops)
    
    # Create and generate a word cloud image
    wordcloud = WordCloud(
        width=1600, 
        height=800,
        background_color='white',
        stopwords=stop_words,
        min_font_size=10,
        max_font_size=150
    ).generate(text)
    
    # Display the word cloud
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Clinical Notes')
    
    # Save the image
    plt.savefig('clinical_notes_wordcloud.png', bbox_inches='tight', dpi=300)
    print("Word cloud saved as 'clinical_notes_wordcloud.png'")
    

if __name__ == "__main__":
    count_notes_per_region()




    
