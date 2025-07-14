
import streamlit as st
import pandas as pd
import numpy as np
import time
import logging
from news_fetcher import NewsFetcher  # Ensure this module exists
from preprocessor import NewsPreprocessor  # Ensure this module exists
from recommender import NewsRecommender  # Ensure this module exists
import plotly.express as px
import os
from typing import List, Optional
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize session state
def initialize_session_state():
    if 'user_id' not in st.session_state:
        logger.debug("Initializing session state")
        st.session_state.user_id = str(np.random.randint(100000, 999999))
        st.session_state.liked_articles = []
        st.session_state.disliked_articles = []
        st.session_state.recommendations = pd.DataFrame()
        st.session_state.news_data = pd.DataFrame()
        try:
            st.session_state.preprocessor = NewsPreprocessor()
            st.session_state.recommender = NewsRecommender()
        except Exception as e:
            logger.error(f"Error initializing preprocessor or recommender: {str(e)}")
            st.error(f"Failed to initialize system components: {str(e)}")
        st.session_state.initialized = False

# Initialize the system
@st.cache_data(show_spinner=False)
def initialize_system(api_key: str) -> bool:
    if not st.session_state.initialized and api_key:
        try:
            with st.spinner('Fetching news data... This may take a minute.'):
                logger.debug(f"Fetching news with API key: {api_key[:4]}...")
                fetcher = NewsFetcher(api_key=api_key)
                categories = ['business', 'technology', 'science', 'health', 'entertainment', 'sports']
                news_dfs = []
                
                # Progress bar for fetching news
                progress_bar = st.progress(0)
                for i, category in enumerate(categories):
                    try:
                        category_news = fetcher.fetch_news_by_category(category=category, page_size=20)
                        if not category_news.empty:
                            category_news['category'] = category
                            news_dfs.append(category_news)
                        else:
                            logger.warning(f"No news fetched for category {category}")
                        time.sleep(0.5)
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 429:
                            st.warning(f"Rate limit hit for category {category}. Waiting and retrying...")
                            logger.warning(f"Rate limit hit for {category}: {str(e)}")
                            time.sleep(5)
                            continue
                        else:
                            logger.error(f"HTTP error for category {category}: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error fetching news for category {category}: {str(e)}")
                    progress_bar.progress((i + 1) / len(categories))
                
                if not news_dfs:
                    st.error("No news data fetched. Please check your API key or internet connection.")
                    logger.error("No news data fetched")
                    return False
                
                # Combine all news
                all_news = pd.concat(news_dfs, ignore_index=True)
                
                # Preprocess the data
                logger.debug("Preprocessing news data")
                all_news = st.session_state.preprocessor.preprocess_dataframe(all_news)
                
                # Add a fake popularity score for demonstration
                all_news['popularity'] = np.random.randint(1, 100, size=len(all_news))
                
                # Fit the vectorizer
                logger.debug("Fitting vectorizer")
                st.session_state.preprocessor.fit_vectorizer(all_news['processed_text'])
                
                # Load data into recommender
                logger.debug("Loading data into recommender")
                st.session_state.recommender.load_data(all_news, st.session_state.preprocessor.vectorizer)
                
                st.session_state.news_data = all_news
                st.session_state.initialized = True
                st.success("News data loaded successfully!")
                logger.debug("System initialized successfully")
                return True
        except Exception as e:
            st.error(f"Failed to initialize system: {str(e)}")
            logger.error(f"System initialization failed: {str(e)}")
            return False
    return st.session_state.initialized

# Validate image URL
def is_valid_image_url(url: Optional[str]) -> bool:
    if not url or not isinstance(url, str):
        return False
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower()
    except requests.RequestException:
        return False

# Generate word cloud
@st.cache_data(show_spinner=False)
def generate_word_cloud(text_series: pd.Series, title: str):
    if text_series.empty:
        return None
    text = ' '.join(text_series.dropna())
    if not text.strip():
        return None
    wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(title)
    ax.axis('off')
    return fig

# Streamlit app
def main():
    logger.debug("Starting main function")
    initialize_session_state()
    
    try:
        st.title("📰 NewTailor - Personalized News Recommender System")
        st.markdown("""
        Welcome to your personalized news feed! This system learns your preferences based on the articles you like
        and dislike, and recommends articles you might find interesting.
        """)
    except Exception as e:
        logger.error(f"Error rendering title/markdown: {str(e)}")
        st.error("Failed to render the app. Please check the logs for details.")
        return
    
    # Sidebar for API key input
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your NewsAPI key:", type="password", help="Get your key from https://newsapi.org")
        
        if st.button("Initialize System"):
            if api_key:
                initialize_system(api_key)
            else:
                st.error("Please provide a valid NewsAPI key.")
        
        if st.session_state.initialized:
            st.markdown("---")
            st.markdown(f"Your user ID: `{st.session_state.user_id}`")
            
            if st.button("Reset My Preferences"):
                st.session_state.liked_articles = []
                st.session_state.disliked_articles = []
                st.session_state.recommendations = pd.DataFrame()
                st.success("Your preferences have been reset!")
    
    if not st.session_state.initialized:
        st.warning("Please enter your NewsAPI key and initialize the system in the sidebar.")
        return
    
    # Main content
    try:
        tab1, tab2, tab3 = st.tabs(["Browse News", "My Recommendations", "My Profile"])
    except Exception as e:
        logger.error(f"Error creating tabs: {str(e)}")
        st.error("Failed to create tabs. Please check the logs.")
        return
    
    with tab1:
        st.header("Browse All News Articles")
        
        # Filter by category
        categories = sorted(st.session_state.news_data['category'].unique())
        selected_category = st.selectbox("Filter by category:", ['All'] + list(categories))
        
        if selected_category != 'All':
            filtered_news = st.session_state.news_data[st.session_state.news_data['category'] == selected_category]
        else:
            filtered_news = st.session_state.news_data
        
        if filtered_news.empty:
            st.info("No articles available in this category.")
        else:
            for idx, row in filtered_news.iterrows():
                with st.expander(f"{row['title']} ({row['category'].capitalize()})"):
                    st.markdown(f"**Source:** {row['source']['name'] if isinstance(row['source'], dict) else row['source']}")
                    st.markdown(f"**Published At:** {row['publishedAt']}")
                    
                    if is_valid_image_url(row.get('urlToImage')):
                        st.image(row['urlToImage'], width=300, caption="Article Image")
                    
                    st.markdown(f"**Description:** {row['description']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"👍 Like", key=f"like_{idx}"):
                            if idx not in st.session_state.liked_articles:
                                st.session_state.liked_articles.append(idx)
                                st.session_state.recommender.update_user_profile(
                                    st.session_state.user_id,
                                    st.session_state.liked_articles,
                                    st.session_state.disliked_articles
                                )
                                st.success("Added to your liked articles!")
                    
                    with col2:
                        if st.button(f"👎 Dislike", key=f"dislike_{idx}"):
                            if idx not in st.session_state.disliked_articles:
                                st.session_state.disliked_articles.append(idx)
                                st.session_state.recommender.update_user_profile(
                                    st.session_state.user_id,
                                    st.session_state.liked_articles,
                                    st.session_state.disliked_articles
                                )
                                st.success("Added to your disliked articles!")
                    
                    st.markdown(f"[Read full article]({row['url']})", unsafe_allow_html=True)
    
    with tab2:
        st.header("Your Personalized Recommendations")
        
        if not st.session_state.liked_articles:
            st.info("Like some articles in the 'Browse News' tab to get personalized recommendations!")
        else:
            # Add recommendation customization
            col1, col2 = st.columns(2)
            with col1:
                rec_count = st.slider("Number of recommendations", 3, 20, 5)
            with col2:
                diversity = st.slider("Diversity level", 0.0, 1.0, 0.3, help="Higher diversity shows more varied articles.")
            
            # Get recommendations
            try:
                recommendations = st.session_state.recommender.get_diverse_recommendations(
                    st.session_state.user_id,
                    top_n=rec_count,
                    diversity=diversity
                )
                
                if recommendations.empty:
                    st.warning("No recommendations available. Try liking more articles.")
                else:
                    st.subheader(f"Recommended For You ({len(recommendations)} articles)")
                    
                    for idx, row in recommendations.iterrows():
                        with st.container():
                            st.markdown(f"### {row['title']}")
                            st.caption(f"Category: {row['category'].capitalize()} | Source: {row.get('source', {}).get('name', 'Unknown')}")
                            
                            if is_valid_image_url(row.get('urlToImage')):
                                st.image(row['urlToImage'], width=300, caption="Article Image")
                            
                            st.markdown(row['description'])
                            
                            # Action buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("👍 Like", key=f"rec_like_{idx}"):
                                    if idx not in st.session_state.liked_articles:
                                        st.session_state.liked_articles.append(idx)
                                        st.session_state.recommender.update_user_profile(
                                            st.session_state.user_id,
                                            st.session_state.liked_articles,
                                            st.session_state.disliked_articles
                                        )
                                        st.success("Added to your liked articles!")
                                        st.rerun()
                            with col2:
                                if st.button("👎 Dislike", key=f"rec_dislike_{idx}"):
                                    if idx not in st.session_state.disliked_articles:
                                        st.session_state.disliked_articles.append(idx)
                                        st.session_state.recommender.update_user_profile(
                                            st.session_state.user_id,
                                            st.session_state.liked_articles,
                                            st.session_state.disliked_articles
                                        )
                                        st.success("Added to your disliked articles!")
                                        st.rerun()
                            
                            st.markdown(f"[Read full article]({row['url']})", unsafe_allow_html=True)
                            st.divider()
            
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
                logger.error(f"Recommendation error: {str(e)}")
                st.info("Try refreshing the page or liking more articles.")
    
    with tab3:
        st.header("Your News Profile")
        
        if not st.session_state.liked_articles and not st.session_state.disliked_articles:
            st.info("You haven't liked or disliked any articles yet. Start browsing to build your profile!")
        else:
            # Summary statistics
            st.subheader("Your Activity Summary")
            st.markdown(f"📖 **Articles Liked:** {len(st.session_state.liked_articles)}")
            st.markdown(f"🚫 **Articles Disliked:** {len(st.session_state.disliked_articles)}")
            
            # Category Distribution Bar Chart
            st.subheader("Category Preferences")
            valid_liked = [idx for idx in st.session_state.liked_articles if idx in st.session_state.news_data.index]
            valid_disliked = [idx for idx in st.session_state.disliked_articles if idx in st.session_state.news_data.index]
            
            if valid_liked or valid_disliked:
                category_data = []
                if valid_liked:
                    liked_counts = st.session_state.news_data.iloc[valid_liked]['category'].value_counts().reset_index()
                    liked_counts.columns = ['category', 'liked_count']
                    liked_counts['type'] = 'Liked'
                    category_data.append(liked_counts)
                if valid_disliked:
                    disliked_counts = st.session_state.news_data.iloc[valid_disliked]['category'].value_counts().reset_index()
                    disliked_counts.columns = ['category', 'disliked_count']
                    disliked_counts['type'] = 'Disliked'
                    category_data.append(disliked_counts)
                
                if category_data:
                    category_df = pd.concat(category_data, ignore_index=True).fillna(0)
                    if 'liked_count' not in category_df:
                        category_df['liked_count'] = 0
                    if 'disliked_count' not in category_df:
                        category_df['disliked_count'] = 0
                    category_df = category_df.groupby(['category', 'type']).sum().reset_index()
                    
                    fig = px.bar(
                        category_df,
                        x='category',
                        y=['liked_count', 'disliked_count'],
                        barmode='group',
                        title="Liked vs Disliked Articles by Category",
                        labels={'value': 'Number of Articles', 'category': 'Category'},
                        color_discrete_map={'liked_count': '#00CC96', 'disliked_count': '#EF553B'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No valid category data available.")
            
            # Word Cloud for Liked and Disliked Articles
            st.subheader("Top Keywords in Your Preferences")
            col1, col2 = st.columns(2)
            with col1:
                if valid_liked:
                    liked_text = st.session_state.news_data.iloc[valid_liked]['processed_text']
                    wordcloud_fig = generate_word_cloud(liked_text, "Keywords in Liked Articles")
                    if wordcloud_fig:
                        st.pyplot(wordcloud_fig)
                    else:
                        st.info("No text data available for liked articles.")
                else:
                    st.info("No liked articles for keyword analysis.")
            
            with col2:
                if valid_disliked:
                    disliked_text = st.session_state.news_data.iloc[valid_disliked]['processed_text']
                    wordcloud_fig = generate_word_cloud(disliked_text, "Keywords in Disliked Articles")
                    if wordcloud_fig:
                        st.pyplot(wordcloud_fig)
                    else:
                        st.info("No text data available for disliked articles.")
                else:
                    st.info("No disliked articles for keyword analysis.")
            
            # Time-Based Analysis
            st.subheader("Publication Date Analysis")
            if valid_liked or valid_disliked:
                time_data = []
                if valid_liked:
                    liked_dates = pd.to_datetime(st.session_state.news_data.iloc[valid_liked]['publishedAt'])
                    liked_dates = liked_dates.dt.date.value_counts().reset_index()
                    liked_dates.columns = ['date', 'count']
                    liked_dates['type'] = 'Liked'
                    time_data.append(liked_dates)
                if valid_disliked:
                    disliked_dates = pd.to_datetime(st.session_state.news_data.iloc[valid_disliked]['publishedAt'])
                    disliked_dates = disliked_dates.dt.date.value_counts().reset_index()
                    disliked_dates.columns = ['date', 'count']
                    disliked_dates['type'] = 'Disliked'
                    time_data.append(disliked_dates)
                
                if time_data:
                    time_df = pd.concat(time_data, ignore_index=True)
                    fig = px.line(
                        time_df,
                        x='date',
                        y='count',
                        color='type',
                        title="Liked vs Disliked Articles Over Time",
                        labels={'date': 'Publication Date', 'count': 'Number of Articles'},
                        color_discrete_map={'Liked': '#00CC96', 'Disliked': '#EF553B'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No valid date data available.")
            
            # Detailed Tables
            st.subheader("Detailed Article Analysis")
            if valid_liked:
                st.write("Liked Articles")
                liked_df = st.session_state.news_data.iloc[valid_liked][['title', 'category', 'source', 'publishedAt', 'url']]
                liked_df['source'] = liked_df['source'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
                liked_df['publishedAt'] = pd.to_datetime(liked_df['publishedAt']).dt.strftime('%Y-%m-%d')
                st.dataframe(liked_df.rename(columns={'title': 'Title', 'category': 'Category', 'source': 'Source', 'publishedAt': 'Published Date', 'url': 'URL'}))
            
            if valid_disliked:
                st.write("Disliked Articles")
                disliked_df = st.session_state.news_data.iloc[valid_disliked][['title', 'category', 'source', 'publishedAt', 'url']]
                disliked_df['source'] = disliked_df['source'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
                disliked_df['publishedAt'] = pd.to_datetime(disliked_df['publishedAt']).dt.strftime('%Y-%m-%d')
                st.dataframe(disliked_df.rename(columns={'title': 'Title', 'category': 'Category', 'source': 'Source', 'publishedAt': 'Published Date', 'url': 'URL'}))
            
            # Summary Table
            st.subheader("Category Preference Summary")
            if valid_liked or valid_disliked:
                summary_data = []
                categories = st.session_state.news_data['category'].unique()
                for category in categories:
                    liked_count = len([idx for idx in valid_liked if st.session_state.news_data.iloc[idx]['category'] == category])
                    disliked_count = len([idx for idx in valid_disliked if st.session_state.news_data.iloc[idx]['category'] == category])
                    total = liked_count + disliked_count
                    liked_pct = (liked_count / total * 100) if total > 0 else 0
                    disliked_pct = (disliked_count / total * 100) if total > 0 else 0
                    summary_data.append({
                        'Category': category.capitalize(),
                        'Liked': liked_count,
                        'Disliked': disliked_count,
                        'Liked %': f"{liked_pct:.1f}%",
                        'Disliked %': f"{disliked_pct:.1f}%"
                    })
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df)
            else:
                st.info("No category data available for summary.")
            
            # Export to CSV
            st.subheader("Export Your Profile")
            if valid_liked or valid_disliked:
                export_data = []
                if valid_liked:
                    liked_df = st.session_state.news_data.iloc[valid_liked][['title', 'category', 'source', 'publishedAt', 'url', 'description']]
                    liked_df['source'] = liked_df['source'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
                    liked_df['publishedAt'] = pd.to_datetime(liked_df['publishedAt']).dt.strftime('%Y-%m-%d')
                    liked_df['status'] = 'Liked'
                    export_data.append(liked_df)
                if valid_disliked:
                    disliked_df = st.session_state.news_data.iloc[valid_disliked][['title', 'category', 'source', 'publishedAt', 'url', 'description']]
                    disliked_df['source'] = disliked_df['source'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
                    disliked_df['publishedAt'] = pd.to_datetime(disliked_df['publishedAt']).dt.strftime('%Y-%m-%d')
                    disliked_df['status'] = 'Disliked'
                    export_data.append(disliked_df)
                
                if export_data:
                    export_df = pd.concat(export_data, ignore_index=True)
                    export_df = export_df.rename(columns={
                        'title': 'Title',
                        'category': 'Category',
                        'source': 'Source',
                        'publishedAt': 'Published Date',
                        'url': 'URL',
                        'description': 'Description',
                        'status': 'Status'
                    })
                    csv_buffer = io.StringIO()
                    export_df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    st.download_button(
                        label="Download Profile as CSV",
                        data=csv_data,
                        file_name=f"user_profile_{st.session_state.user_id}.csv",
                        mime="text/csv",
                        key="download_profile_csv"
                    )
                else:
                    st.info("No data available to export.")
            else:
                st.info("No data available to export.")

if __name__ == "__main__":
    logger.debug("Running Streamlit app")
    main()