import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import content_data

print("=== INSPECTING FIRST 10 VIDEOS (18-25) ===")
vids_18 = [v for v in content_data.VIDEO_PRACTICE_ITEMS if v.get("age_group") == "18-25"]
for i, v in enumerate(vids_18[:10]):
    print(f"[{i}] ID: {v.get('id')} | Title: {v.get('title')}")
    print(f"    YT ID: {v.get('youtube_id')} | Embed: {v.get('youtubeEmbedUrl')}")
    print(f"    Clue: {v.get('clue')}")
    print(f"    Questions: {v.get('guiding_questions')}")
    print(f"    Keywords: {v.get('suggested_keywords')}")
    print("-" * 50)

print("\n=== INSPECTING FIRST 10 IMAGES (18-25) ===")
imgs_18 = [im for im in content_data.IMAGE_PRACTICE_ITEMS if im.get("age_group") == "18-25"]
for i, im in enumerate(imgs_18[:10]):
    print(f"[{i}] ID: {im.get('id')} | Title: {im.get('title')}")
    print(f"    URL: {im.get('image_url')}")
    print(f"    Clue: {im.get('clue')}")
    print(f"    Questions: {im.get('guiding_questions')}")
    print(f"    Keywords: {im.get('suggested_keywords')}")
    print("-" * 50)
