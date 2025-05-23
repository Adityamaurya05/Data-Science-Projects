# combine_datasets.py
import pandas as pd

# Load the datasets
true_news = pd.read_csv("True.csv")
fake_news = pd.read_csv("Fake.csv")

# Add labels
true_news['label'] = 'REAL'
fake_news['label'] = 'FAKE'

# Combine
combined = pd.concat([true_news, fake_news])

# Shuffle the dataset
combined = combined.sample(frac=1).reset_index(drop=True)

# Save combined dataset
combined.to_csv("news.csv", index=False)