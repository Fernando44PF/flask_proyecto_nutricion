import requests
from models.youtube_model import YouTubeVideo

API_KEY = "AIzaSyCv07KwHW3vgHk7-7sSAvncX4ILNHNkKlQ"

def search_youtube(query):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 6,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    videos = []

    for item in data.get("items", []):
        snippet = item["snippet"]
        video = YouTubeVideo(
            title=snippet["title"],
            channel=snippet["channelTitle"],
            video_id=item["id"]["videoId"],
            thumbnail=snippet["thumbnails"]["medium"]["url"]
        )
        videos.append(video)

    return videos
