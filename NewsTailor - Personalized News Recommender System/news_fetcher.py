import requests
import pandas as pd
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_news(self, query=None, language='en', page_size=100):
        # Get news from the last 7 days
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        params = {
            'apiKey': self.api_key,
            'language': language,
            'pageSize': page_size,
            'from': from_date,
            'sortBy': 'publishedAt'
        }
        
        if query:
            params['q'] = query
            
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return pd.DataFrame(articles)
        else:
            print(f"Error fetching news: {response.status_code}")
            return pd.DataFrame()
    
    def fetch_news_by_category(self, category, language='en', page_size=100):
        url = "https://newsapi.org/v2/top-headlines"
        
        params = {
            'apiKey': self.api_key,
            'category': category,
            'language': language,
            'pageSize': page_size
        }
            
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return pd.DataFrame(articles)
        else:
            print(f"Error fetching news: {response.status_code}")
            return pd.DataFrame()

# Example usage:
# fetcher = NewsFetcher(api_key='YOUR_API_KEY')
# tech_news = fetcher.fetch_news(query='technology')
# business_news = fetcher.fetch_news_by_category(category='business')