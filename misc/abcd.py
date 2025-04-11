import pandas as pd
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize

# Download the sentence tokenizer (if you haven't already)
nltk.download('punkt')

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
            sentences = sent_tokenize(text)
            all_sentences.extend(sentences)

    sentence_frequencies = Counter(all_sentences)
    return sentence_frequencies

# --- Example Usage ---
csv_file_path = r'clinician_notes.csv'  # Replace 'your_file.csv' with the actual path
frequencies = get_sentence_frequencies(csv_file_path)

# Print the most common sentences
print("Most frequent sentences:")
for sentence, count in frequencies.most_common(10):  # Print top 10
    print(f"- {sentence}: {count}")

# #You can also access the frequency of a specific sentence:
# print(f"\nFrequency of a particular sentence: {frequencies['The patient is stable.']}")

# #If you want to see all sentence frequencies:
# print("\nAll sentence frequencies:")
# print(frequencies)