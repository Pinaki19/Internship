from collections import Counter
import re
from nltk.corpus import stopwords
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from predict import predict_label
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS,CountVectorizer
import seaborn as sns
import os
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, ttest_ind

cur_dir=os.path.dirname(__file__)
os.chdir(cur_dir)

# Load the clinical notes ( Q 1)
data = pd.read_csv(r'.\CSV\clinician_notes.csv')


#Question 2
def count_notes_per_region():
    # Read the CSV files
    notes_df = pd.read_csv(r'.\CSV\clinician_notes.csv')
    regions_df = pd.read_csv(r'.\CSV\regions_data.csv')

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
    result.to_csv(r'.\results\notes_per_region.csv', index=False)

    # Print results
    print("\nNotes per Region:")
    print("================")
    for _, row in result.iterrows():
        print(f"{row['region_name']} (ID: {row['region_id']}): {row['note_count']} notes")

#Part of Q2
def analyze_notes_frequency_over_time():
    # Read the necessary files
    notes_df = pd.read_csv(r'.\CSV\clinician_notes.csv')
    trials_df = pd.read_csv(r'.\CSV\trial_results.csv')

    # Convert dates to datetime
    notes_df['note_date'] = pd.to_datetime(notes_df['note_date'], format='%d-%m-%Y')
    trials_df['visit_date'] = pd.to_datetime(trials_df['visit_date'], format='%d-%m-%Y')

    # Get trial duration
    trial_start = trials_df['visit_date'].min()
    trial_end = trials_df['visit_date'].max()

    # Group notes by region and month
    notes_df['month'] = notes_df['note_date'].dt.to_period('M')
    frequency = notes_df.groupby(['region_id', 'month']).size().reset_index(name='note_count')
    frequency['month'] = frequency['month'].astype(str)

    top_n = 5
    top_regions = (frequency.groupby('region_id')['note_count']
                    .sum()
                    .nlargest(top_n)
                    .index)

    # Filter only top N regions
    top_frequency = frequency[frequency['region_id'].isin(top_regions)]

    plt.figure(figsize=(15, 8))
    for region in top_regions:
        region_data = top_frequency[top_frequency['region_id'] == region]
        plt.plot(region_data['month'], region_data['note_count'], marker='o', label=f'Region {region}')

    plt.title(f'Notes Frequency Over Time (Top {top_n} Regions Only)')
    plt.xlabel('Month')
    plt.ylabel('Number of Notes')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(r'.\results\notes_frequency_top_regions.png')

    # Heatmap for large number of regions
    pivot_df = frequency.pivot(index='region_id', columns='month', values='note_count').fillna(0)

    plt.figure(figsize=(18, 10))
    sns.heatmap(pivot_df, cmap='Blues', linewidths=.5, linecolor='gray')
    plt.title('Notes Frequency Heatmap (Region vs Month)', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Region ID')
    plt.tight_layout()
    plt.savefig(r'.\results\notes_frequency_heatmap.png')

    # Summary statistics
    print("\nNotes Frequency Analysis:")
    print(f"Trial Duration: {trial_start.strftime('%d-%m-%Y')} to {trial_end.strftime('%d-%m-%Y')}")

    monthly_total = frequency.groupby('month')['note_count'].sum()
    print(f"\nBusiest Month: {monthly_total.idxmax()} with {monthly_total.max()} notes")
    print(f"Quietest Month: {monthly_total.idxmin()} with {monthly_total.min()} notes")
    print(f"Average Notes per Month: {monthly_total.mean():.2f}")


#Question 3
def report_top_words(n:int=3):
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
def analyze_sentiment():
    #Perform sentiment analysis
    data['sentiment'] = data['note_text'].apply(predict_label)
    # Save results to CSV
    output_file = r'.\results\sentiment_analysis_results.csv'
    data.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")



def extract_numerical_changes(text):
    # Extract numerical changes using regex
    changes = re.findall(r'(\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?%|\d+(?:\.\d+)?)\s*(?:to|->)\s*(\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?%|\d+(?:\.\d+)?)', text)
    return changes
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

def extract_numerical_changes(text):
    # Dummy implementation — replace with your actual logic
    return []

def analyze_negative_trends():
    # Read and drop duplicate rows
    df = pd.read_csv(r'.\results\sentiment_analysis_results.csv').drop_duplicates()

    # Filter for negative sentiment
    negative_notes = df[df['sentiment'] == 'Negative'].dropna(subset=['note_text'])

    # Drop duplicate texts
    negative_notes = negative_notes.drop_duplicates(subset=['note_text'])

    if len(negative_notes) == 0:
        print("No negative trends found.")
        return

    # Custom stop words
    custom_stop_words = list(set(ENGLISH_STOP_WORDS).union([
        'patient', 'doctor', 'hospital', 'day', 'week', 'note', 'labs', 'requires', 'follow',
        'status', 'chest', 'surgical', 'despite', 'new', 'positive',
         'mental', 'abdominal', 'low', 'exam','shows','review'
    ]))

    vectorizer = TfidfVectorizer(
        max_features=50,
        stop_words=custom_stop_words,
        ngram_range=(1, 2)
    )

    # Fit and transform the negative notes
    tfidf_matrix = vectorizer.fit_transform(negative_notes['note_text'])

    # Use KMeans to cluster the negative notes
    n_clusters = min(4, len(negative_notes))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(tfidf_matrix)

    # Helper to get top terms per cluster
    def get_top_terms(cluster_center, n_terms=5):
        terms = vectorizer.get_feature_names_out()
        sorted_idx = np.argsort(cluster_center)[::-1]
        return [terms[i] for i in sorted_idx[:n_terms]]

    # Group notes by cluster
    trends = {}
    cluster_keywords = []
    for i in range(n_clusters):
        cluster_center = kmeans.cluster_centers_[i]
        top_terms = get_top_terms(cluster_center)
        cluster_keywords.append(top_terms)
        cluster_name = f"Trend Keywords {i+1}: {', '.join(top_terms)}"

        cluster_notes = negative_notes.iloc[np.where(clusters == i)[0]]['note_text'].drop_duplicates().tolist()
        trends[cluster_name] = cluster_notes

    # Print summary
    print("\nNegative Trends Analysis Summary:")
    print("=================================")

    for category, instances in trends.items():
        if instances:
            print(f"\n{category}:")
            print("-" * len(category))
            seen = set()
            for note in instances:
                sentence = sent_tokenize(note)[0]
                if sentence not in seen:
                    seen.add(sentence)
                    changes = extract_numerical_changes(note)
                    if changes:
                        print(f"- {sentence} (Changes: {', '.join([f'{c[0]} to {c[1]}' for c in changes])})")
                    else:
                        print(f"- {sentence}")

    # --------- Adverse Effect Marking (based on TF-IDF similarity) ---------

    

    # Identify clusters considered adverse
    adverse_notes = []
    for i, terms in enumerate(cluster_keywords):
        adverse_notes.extend(trends[f"Trend Keywords {i+1}: {', '.join(terms)}"])

    adverse_notes = list(set(adverse_notes))

    if adverse_notes:
        # Vectorize all notes (adverse + all notes)
        all_texts = df['note_text'].fillna("").tolist()
        combined_texts = adverse_notes + all_texts

        vectorizer_full = TfidfVectorizer(
            max_features=1000,
            stop_words=custom_stop_words,
            ngram_range=(1, 2)
        )
        tfidf_all = vectorizer_full.fit_transform(combined_texts)

        tfidf_adverse = tfidf_all[:len(adverse_notes)]
        tfidf_main = tfidf_all[len(adverse_notes):]

        # Compute similarity
        similarity_matrix = cosine_similarity(tfidf_main, tfidf_adverse)

        # Mark those with high similarity to any adverse cluster note
        threshold = 0.3
        adverse_flags = (similarity_matrix.max(axis=1) >= threshold)

        # Update original DataFrame
        df['adverse_effect'] = adverse_flags
    else:
        df['adverse_effect'] = False

    # Save result
    df.to_csv(r'C:\Users\pinak\Downloads\Internship\main\results\adverse_effects_results.csv', index=False)

    
#Question 5 Wordcloud
def generate_wordcloud():
    df = pd.read_csv(r'.\CSV\clinician_notes.csv')
    # Combine all notes into one text
    text = ' '.join(df['note_text'].astype(str))

    # Get default English stopwords
    stop_words = set(stopwords.words('english'))

    # Use CountVectorizer to find top 20 most common words
    vectorizer = CountVectorizer(stop_words='english')
    word_counts = vectorizer.fit_transform(df['note_text'].astype(str))
    sum_words = word_counts.sum(axis=0)
    word_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    sorted_words = sorted(word_freq, key=lambda x: x[1], reverse=True)
    top_20_words = [word for word, count in sorted_words[:20]]

    # Add the top 20 most frequent words as custom stopwords
    stop_words.update(top_20_words)

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
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Clinical Notes')

    # Save the image
    plt.savefig(r'.\results\clinical_notes_wordcloud.png', bbox_inches='tight', dpi=300)
    print("Word cloud saved as 'clinical_notes_wordcloud.png'")


def Q2():
    count_notes_per_region()
    analyze_notes_frequency_over_time()
    
def Q3():
    report_top_words(3)

def Q4():
    #analyze_sentiment()
    analyze_negative_trends()

def Q5():
    #TODO adverse_event vs Adverse effect from note_text
    generate_wordcloud()

if __name__ == "__main__":
    Q4()
