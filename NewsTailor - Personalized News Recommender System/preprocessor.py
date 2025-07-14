import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')  # Required for WordNet Lemmatizer
nltk.download('punkt_tab')

class NewsPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(max_features=5000)
    
    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters and numbers
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def preprocess_text(self, text):
        text = self.clean_text(text)
        # Tokenize
        words = nltk.word_tokenize(text)
        # Remove stopwords and lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        return ' '.join(words)
    
    def preprocess_dataframe(self, df):
        # Handle missing values
        df = df.dropna(subset=['title', 'description', 'content'])
        df = df.fillna('')
        
        # Combine title, description, and content for better representation
        df['combined_text'] = df['title'] + ' ' + df['description'] + ' ' + df['content']
        
        # Preprocess the combined text
        df['processed_text'] = df['combined_text'].apply(self.preprocess_text)
        
        return df
    
    def fit_vectorizer(self, texts):
        self.vectorizer.fit(texts)
    
    def transform_text_to_features(self, texts):
        return self.vectorizer.transform(texts)