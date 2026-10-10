import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import urllib.request
import urllib.error
import json
from content_data import THERAPY_VIDEOS

print(f"Total therapy videos: {len(THERAPY_VIDEOS)}")

results = []
for v in THERAPY_VIDEOS:
    vid_id = v.get("youtube_id", "")
    thumb = v.get("thumbnail", "")
    title = v.get("title", "")
    source = v.get("source", "")
    item_id = v.get("id", "")
    
    # Check YouTube oEmbed to see if the video ID is valid on YouTube
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid_id}&format=json"
    is_valid_yt = False
    yt_title = ""
    try:
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                is_valid_yt = True
                data = json.loads(resp.read().decode('utf-8'))
                yt_title = data.get('title', '')
    except Exception as e:
        yt_title = f"Error: {e}"

    results.append({
        "id": item_id,
        "title": title,
        "youtube_id": vid_id,
        "thumbnail": thumb,
        "is_valid_yt": is_valid_yt,
        "yt_title": yt_title
    })

print(json.dumps(results, indent=2))
