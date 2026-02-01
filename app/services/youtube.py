import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"

async def get_channel_id_from_url(url: str, client: httpx.AsyncClient):
    """
    Logic: handle handles and channel IDs asynchronously.
    """
    if "@" in url:
        handle = url.split("@")[1].split("/")[0]
        params = {
            "q": handle,
            "part": "id",
            "type": "channel",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY
        }
        res = await client.get(f"{BASE_URL}/search", params=params)
        data = res.json()
        
        if not data.get('items'):
            return None
        return data['items'][0]['id']['channelId']
    
    # Simple split logic for /channel/ URLs
    return url.split("channel/")[1].split("/")[0]

async def get_channel_context(channel_url: str):
    """
    Logic: Fetch channel bio and recent activity using an async client.
    """
    async with httpx.AsyncClient() as client:
        channel_id = await get_channel_id_from_url(channel_url, client)
        
        # 1. Get Channel Snippet (About section)
        ch_params = {"part": "snippet", "id": channel_id, "key": YOUTUBE_API_KEY}
        ch_res = await client.get(f"{BASE_URL}/channels", params=ch_params)
        snippet = ch_res.json()['items'][0]['snippet']
        
        # 2. Get last 5 videos for niche context
        search_params = {
            "channelId": channel_id,
            "part": "snippet",
            "order": "date",
            "maxResults": 5,
            "key": YOUTUBE_API_KEY
        }
        vid_res = await client.get(f"{BASE_URL}/search", params=search_params)
        titles = [item['snippet']['title'] for item in vid_res.json().get('items', [])]
        
        return {
            "channel_id": channel_id,
            "title": snippet['title'],
            "description": snippet['description'],
            "recent_titles": titles
        }

async def find_top_competitors(search_queries: list, original_channel_id: str):
    """
    Logic: Run keyword searches in parallel to find unique competitors.
    """
    competitors = []
    seen_ids = {original_channel_id}

    async with httpx.AsyncClient() as client:
        for query in search_queries:
            params = {
                "q": query,
                "part": "snippet",
                "type": "channel",
                "maxResults": 5,
                "key": YOUTUBE_API_KEY
            }
            res = await client.get(f"{BASE_URL}/search", params=params)
            items = res.json().get('items', [])

            for item in items:
                cid = item['id']['channelId']
                if cid not in seen_ids:
                    seen_ids.add(cid)
                    competitors.append({
                        "channel_id": cid,
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description']
                    })
            
            if len(competitors) >= 10:
                break

    return competitors[:10]

async def get_channel_performance(channel_id: str):
    """
    THE MASTERPIECE: Efficiently flags viral videos.
    """
    async with httpx.AsyncClient() as client:
        # Step A: Get Uploads Playlist
        ch_params = {"part": "contentDetails", "id": channel_id, "key": YOUTUBE_API_KEY}
        ch_res = await client.get(f"{BASE_URL}/channels", params=ch_params)
        uploads_id = ch_res.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Step B: Get last 20 videos
        pl_params = {"part": "contentDetails,snippet", "playlistId": uploads_id, "maxResults": 20, "key": YOUTUBE_API_KEY}
        pl_res = await client.get(f"{BASE_URL}/playlistItems", params=pl_params)
        video_ids = [item['contentDetails']['videoId'] for item in pl_res.json().get('items', [])]

        # Step C: Get Stats in 1 batch call
        v_params = {"part": "statistics,snippet", "id": ",".join(video_ids), "key": YOUTUBE_API_KEY}
        stats_res = await client.get(f"{BASE_URL}/videos", params=v_params)
        
        video_stats = []
        total_views = 0
        items = stats_res.json().get('items', [])

        for vid in items:
            views = int(vid['statistics'].get('viewCount', 0))
            video_stats.append({
                "title": vid['snippet']['title'],
                "views": views,
                "url": f"https://youtube.com/watch?v={vid['id']}"
            })
            total_views += views

        avg_views = total_views / len(video_stats) if video_stats else 0
        outperformers = []

        for vid in video_stats:
            if vid['views'] > (avg_views * 1.5):
                score = vid['views'] / avg_views
                vid['outperformance_score'] = round(score, 2)
                outperformers.append(vid)

        return sorted(outperformers, key=lambda x: x['outperformance_score'], reverse=True)[:3]