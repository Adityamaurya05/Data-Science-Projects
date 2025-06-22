import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from wordcloud import WordCloud
import pandas as pd
import streamlit as st
from utils.data_fetcher import get_trending_videos, get_category_mapping

def plot_boxplot_outliers(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='category_name', y='view_count')
    plt.xticks(rotation=45)
    plt.title('View Count Distribution by Category (Outlier Detection)')
    st.pyplot(fig)

def plot_time_series(df):
    if 'timestamp' in df.columns:
        # Historical data
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        ts_data = df.groupby('date').agg({
            'view_count': 'mean',
            'like_count': 'mean',
            'comment_count': 'mean'
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ts_data.plot(ax=ax)
        plt.title('Daily Average Metrics Over Time')
        st.pyplot(fig)
    else:
        # Current data by hour
        hr_data = df.groupby('publish_hour').agg({
            'view_count': 'mean',
            'like_count': 'mean',
            'comment_count': 'mean'
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        hr_data.plot(ax=ax)
        plt.title('Metrics by Publish Hour')
        st.pyplot(fig)

def plot_network_graph(df):
    # Create channel-video network
    G = nx.Graph()
    
    # Add nodes and edges
    for _, row in df.iterrows():
        G.add_node(row['channel_title'], type='channel')
        G.add_node(row['video_id'], type='video')
        G.add_edge(row['channel_title'], row['video_id'])
    
    # Draw graph
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)
    
    # Color nodes by type
    node_colors = []
    for node in G.nodes():
        if G.nodes[node]['type'] == 'channel':
            node_colors.append('red')
        else:
            node_colors.append('blue')
    
    nx.draw(G, pos, node_color=node_colors, node_size=50, with_labels=False)
    plt.title('Channel-Video Network Graph')
    st.pyplot(plt)

def plot_sentiment_analysis(df):
    # Sentiment distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.histplot(df['title_sentiment'], bins=20, kde=True, ax=ax1)
    ax1.set_title('Title Sentiment Distribution')
    
    sns.histplot(df['description_sentiment'], bins=20, kde=True, ax=ax2)
    ax2.set_title('Description Sentiment Distribution')
    
    st.pyplot(fig)
    
    # Word cloud of positive/negative titles
    st.subheader("Word Clouds")
    
    pos_titles = ' '.join(df[df['title_sentiment'] > 0]['title'])
    neg_titles = ' '.join(df[df['title_sentiment'] < 0]['title'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Positive Titles**")
        if pos_titles:
            wordcloud = WordCloud(width=400, height=300).generate(pos_titles)
            plt.figure(figsize=(8, 6))
            plt.imshow(wordcloud)
            plt.axis("off")
            st.pyplot(plt)
    
    with col2:
        st.write("**Negative Titles**")
        if neg_titles:
            wordcloud = WordCloud(width=400, height=300).generate(neg_titles)
            plt.figure(figsize=(8, 6))
            plt.imshow(wordcloud)
            plt.axis("off")
            st.pyplot(plt)