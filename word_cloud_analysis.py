
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk

# Download stopwords
nltk.download('stopwords')

# Read the clinical notes
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
