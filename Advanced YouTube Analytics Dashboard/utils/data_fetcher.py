from googleapiclient.discovery import build
import isodate
import pandas as pd

def get_trending_videos(api_key, max_results=200):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    
    try:
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            chart='mostPopular',
            regionCode='US',
            maxResults=min(50, max_results)
        )
        while request and len(videos) < max_results:
            response = request.execute()
            videos.extend(response.get('items', []))
            request = youtube.videos().list_next(request, response)
            
    except Exception as e:
        print(f"🚨 API Error: {str(e)}")
    
    return videos[:max_results]

def get_category_mapping(api_key, region='US'):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode=region
    )
    response = request.execute()
    return {int(item['id']): item['snippet']['title'] for item in response['items']}