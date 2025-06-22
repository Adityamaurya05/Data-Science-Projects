import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import isodate
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="🎬 Advanced YouTube Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .st-b7 {color: #ff4b4b;}
    .st-cj {background-color: #e6f3ff;}
    .metric-card {border-radius: 10px; padding: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .title-font {font-family: 'Helvetica Neue', sans-serif; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Helper Functions
def fetch_data(api_key, max_results=50, region='US'):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        regionCode=region,
        maxResults=max_results
    )
    return request.execute().get('items', [])

def process_videos(videos):
    processed = []
    for video in videos:
        try:
            # Safely extract data with fallbacks
            item = {
                'id': video.get('id', ''),
                'title': video.get('snippet', {}).get('title', 'No Title'),
                'published_at': pd.to_datetime(video.get('snippet', {}).get('publishedAt', None)),
                'channel': video.get('snippet', {}).get('channelTitle', 'Unknown'),
                'views': int(video.get('statistics', {}).get('viewCount', 0)),
                'likes': int(video.get('statistics', {}).get('likeCount', 0)),
                'comments': int(video.get('statistics', {}).get('commentCount', 0)),
                'duration': isodate.parse_duration(video.get('contentDetails', {}).get('duration', 'PT0M')).total_seconds(),
                'tags': video.get('snippet', {}).get('tags', []),
                'category': video.get('snippet', {}).get('categoryId', '0')
            }
            processed.append(item)
        except Exception as e:
            st.warning(f"Skipping video due to error: {str(e)}")
    return pd.DataFrame(processed)

# UI Components
def sidebar_controls():
    with st.sidebar:
        st.title("⚙️ Controls")
        api_key = st.text_input("YouTube API Key", type="password", help="Get from Google Cloud Console")
        
        col1, col2 = st.columns(2)
        with col1:
            max_results = st.slider("Max Videos", 10, 100, 50)
        with col2:
            region = st.selectbox("Region", ['US', 'IN', 'GB', 'BR', 'DE', 'FR'])
        
        if st.button("🚀 Fetch Data", use_container_width=True):
            if api_key and len(api_key) == 39:
                with st.spinner("Fetching trending videos..."):
                    try:
                        videos = fetch_data(api_key, max_results, region)
                        df = process_videos(videos)
                        if not df.empty:
                            df = enhance_data(df)
                            st.session_state.df = df
                            st.session_state.processed = True
                            st.success(f"Fetched {len(df)} videos!")
                        else:
                            st.error("No videos found - try different parameters")
                    except Exception as e:
                        st.error(f"API Error: {str(e)}")
            else:
                st.warning("Please enter a valid API key")
        
        st.divider()
        st.markdown("### 🔍 Filters")
        if st.session_state.processed:
            min_views = st.slider("Minimum Views", 
                                int(st.session_state.df['views'].min()), 
                                int(st.session_state.df['views'].max()),
                                int(st.session_state.df['views'].quantile(0.25)))
            st.session_state.filtered_df = st.session_state.df[st.session_state.df['views'] >= min_views]

def enhance_data(df):
    # Sentiment Analysis
    df['title_sentiment'] = df['title'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
    # Engagement Metrics
    df['engagement'] = (df['likes'] + df['comments']) / df['views'].clip(lower=1)
    df['like_ratio'] = df['likes'] / df['views'].clip(lower=1)
    
    # Time Features
    df['publish_hour'] = df['published_at'].dt.hour
    df['publish_day'] = df['published_at'].dt.day_name()
    
    # Duration Categories
    df['duration_min'] = df['duration'] / 60
    df['duration_type'] = pd.cut(df['duration_min'],
                                bins=[0, 5, 10, 30, 60, 999],
                                labels=['Short (<5m)', 'Medium (5-10m)', 'Long (10-30m)', 'XL (30-60m)', 'XXL (>1h)'])
    return df

# Dashboard Components
def metrics_section():
    if st.session_state.processed:
        df = st.session_state.filtered_df
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📺 Total Videos", len(df))
        with col2:
            st.metric("👀 Avg Views", f"{df['views'].mean():,.0f}")
        with col3:
            st.metric("👍 Avg Likes", f"{df['likes'].mean():,.0f}")
        with col4:
            st.metric("💬 Avg Comments", f"{df['comments'].mean():,.0f}")

def visualization_section():
    if st.session_state.processed:
        df = st.session_state.filtered_df
        
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📊 Distributions", "📌 Engagement", "☁️ Content"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Views Over Time")
                fig = px.line(df.sort_values('published_at'), 
                            x='published_at', y='views',
                            hover_data=['title', 'channel'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Top Channels")
                top_channels = df.groupby('channel')['views'].sum().nlargest(10)
                fig = px.bar(top_channels, orientation='h')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("View Distribution")
                fig = px.box(df, y='views', log_y=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Duration Analysis")
                fig = px.pie(df, names='duration_type')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Engagement Heatmap")
            heatmap_data = df.pivot_table(index='publish_day', 
                                        columns='publish_hour', 
                                        values='engagement', 
                                        aggfunc='mean')
            fig = px.imshow(heatmap_data, color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Title Sentiment")
                fig = px.histogram(df, x='title_sentiment', nbins=20)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Word Cloud")
                text = ' '.join(df['title'].tolist())
                wordcloud = WordCloud(width=800, height=400).generate(text)
                plt.figure(figsize=(12,6))
                plt.imshow(wordcloud)
                plt.axis("off")
                st.pyplot(plt)

def raw_data_section():
    if st.session_state.processed:
        with st.expander("🔍 View Raw Data"):
            st.dataframe(st.session_state.filtered_df.sort_values('views', ascending=False))

# Main App
def main():
    st.title("🎬 Advanced YouTube Analytics Dashboard")
    st.markdown("Analyze trending videos with interactive controls and visualizations")
    
    sidebar_controls()
    
    if st.session_state.processed:
        metrics_section()
        visualization_section()
        raw_data_section()
    else:
        st.info("👈 Enter your API key and fetch data to begin analysis")

if __name__ == "__main__":
    main()