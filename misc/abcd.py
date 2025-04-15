import pandas as pd
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize

import pandas as pd
from collections import Counter
import random


# Load the CSV
df = pd.read_csv(r'C:\Users\pinak\Downloads\Internship\main\results\notes_with_outcomes.csv') 

# Drop rows with missing note_text
df = df.dropna(subset=['note_text'])

# Group by trial_outcome and count note_text entries
note_counts = df.groupby('trial_outcome')['note_text'].count().reset_index()

# Rename for clarity
note_counts.columns = ['trial_outcome', 'note_text_count']
print()
# Print result
print(note_counts)


def get_sentence_frequencies(csv_file):
    """
    Calculates the frequency of each sentence in the 'note_text' column of a CSV file.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        collections.Counter: A Counter object where keys are sentences and 
                           values are their frequencies.
    """

    df = pd.read_csv(csv_file)

    all_sentences = []
    for text in df['note_text']:
        if isinstance(text, str):  # Handle potential non-string values
            #sentences =  sent_tokenize(text)
            all_sentences.append(text)

    sentence_frequencies = Counter(all_sentences)
    return sentence_frequencies

# --- Example Usage ---
csv_file_path = r'C:\Users\pinak\Downloads\Internship\main\results\notes_with_outcomes.csv'  # Replace 'your_file.csv' with the actual path
frequencies = get_sentence_frequencies(csv_file_path)

k,v=0,0
for sentence, count in frequencies.items():  # Print top 10
    k+=1
    v+=count
    
print(f'\nUnique Notes: {k} || Total Notes: {v}')
