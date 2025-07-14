import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
from collections import defaultdict

class NewsRecommender:
    def __init__(self):
        self.news_data = pd.DataFrame()
        self.user_profiles = defaultdict(dict)
        self.vectorizer = None
        self.article_vectors = None
    
    def load_data(self, news_data, vectorizer):
        self.news_data = news_data
        self.vectorizer = vectorizer
        # Convert to array immediately
        self.article_vectors = self.vectorizer.transform(news_data['processed_text']).toarray()
    
    def update_user_profile(self, user_id, liked_articles_indices, disliked_articles_indices=None):
        if liked_articles_indices:
            # Convert to array if it's sparse
            liked_vectors = self.article_vectors[liked_articles_indices]
            if hasattr(liked_vectors, 'toarray'):
                liked_vectors = liked_vectors.toarray()
            self.user_profiles[user_id]['likes'] = np.mean(liked_vectors, axis=0)
        
        if disliked_articles_indices:
            disliked_vectors = self.article_vectors[disliked_articles_indices]
            if hasattr(disliked_vectors, 'toarray'):
                disliked_vectors = disliked_vectors.toarray()
            self.user_profiles[user_id]['dislikes'] = np.mean(disliked_vectors, axis=0)
    
    def recommend_articles(self, user_id, top_n=5):
        if user_id not in self.user_profiles or 'likes' not in self.user_profiles[user_id]:
            return self.news_data.sort_values(by='popularity', ascending=False).head(top_n)
        
        user_likes = self.user_profiles[user_id]['likes']
        
        # Ensure user_likes is a 2D array
        if len(user_likes.shape) == 1:
            user_likes = user_likes.reshape(1, -1)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_likes, self.article_vectors)
        
        # Get top N similar articles
        similar_indices = np.argsort(similarities[0])[-top_n:][::-1]
        
        # Exclude articles the user has already liked
        liked_indices = set()
        if 'liked_articles' in self.user_profiles[user_id]:
            liked_indices = set(self.user_profiles[user_id]['liked_articles'])
        
        recommendations = []
        for idx in similar_indices:
            if idx not in liked_indices:
                recommendations.append(self.news_data.iloc[idx])
                if len(recommendations) >= top_n:
                    break
        
        return pd.DataFrame(recommendations)
    
    def get_similar_articles(self, article_index, top_n=5):
        # Ensure the vector is 2D
        article_vector = self.article_vectors[article_index].reshape(1, -1)
        similarities = cosine_similarity(article_vector, self.article_vectors)
        similar_indices = np.argsort(similarities[0])[-top_n-1:-1][::-1]
        return self.news_data.iloc[similar_indices]
    
    def get_diverse_recommendations(self, user_id, top_n=5, diversity=0.5):
        if user_id not in self.user_profiles or 'likes' not in self.user_profiles[user_id]:
            return self.news_data.sort_values(by='popularity', ascending=False).head(top_n)
        
        user_likes = self.user_profiles[user_id]['likes']
        if len(user_likes.shape) == 1:
            user_likes = user_likes.reshape(1, -1)
        
        similarities = cosine_similarity(user_likes, self.article_vectors)[0]
        
        # Use nearest neighbors with array input
        nn_model = NearestNeighbors(n_neighbors=top_n*5, metric='cosine')
        nn_model.fit(self.article_vectors)
        
        # Find diverse recommendations
        _, indices = nn_model.kneighbors(user_likes, n_neighbors=top_n*5)
        candidate_indices = indices[0]
        
        # Select based on similarity and diversity
        selected_indices = []
        remaining_indices = list(candidate_indices)
        
        if remaining_indices:
            selected_indices.append(remaining_indices.pop(0))
        
        while len(selected_indices) < top_n and remaining_indices:
            diversity_scores = []
            for idx in remaining_indices:
                if len(selected_indices) == 0:
                    diversity_score = 1
                else:
                    # Calculate using arrays
                    selected_vectors = self.article_vectors[selected_indices]
                    mean_vector = np.mean(selected_vectors, axis=0).reshape(1, -1)
                    current_vector = self.article_vectors[idx].reshape(1, -1)
                    diversity_score = 1 - cosine_similarity(
                        current_vector,
                        mean_vector
                    )[0][0]
                
                combined_score = diversity * diversity_score + (1 - diversity) * similarities[idx]
                diversity_scores.append(combined_score)
            
            best_idx = remaining_indices[np.argmax(diversity_scores)]
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)
        
        return self.news_data.iloc[selected_indices]