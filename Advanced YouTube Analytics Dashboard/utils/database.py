import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('youtube_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (video_id TEXT PRIMARY KEY,
                  title TEXT,
                  channel_title TEXT,
                  category_name TEXT,
                  view_count INTEGER,
                  like_count INTEGER,
                  comment_count INTEGER,
                  duration_sec REAL,
                  publish_hour INTEGER,
                  engagement_rate REAL,
                  title_sentiment REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_to_db(df):
    init_db()
    conn = sqlite3.connect('youtube_data.db')
    df.to_sql('videos', conn, if_exists='append', index=False)
    conn.close()

def get_historical_data(days=7):
    init_db()
    conn = sqlite3.connect('youtube_data.db')
    query = f"""SELECT * FROM videos 
                WHERE timestamp >= datetime('now', '-{days} days')"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df