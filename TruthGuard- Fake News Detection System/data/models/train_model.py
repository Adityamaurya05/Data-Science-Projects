import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle

# Load preprocessed data
df = pd.read_csv("processed_news.csv")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    df['processed_text'], 
    df['label'], 
    test_size=0.2, 
    random_state=42
)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Initialize and train model
model = PassiveAggressiveClassifier(max_iter=50)
model.fit(X_train_tfidf, y_train)

# Predict and evaluate
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

# Save model and vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)