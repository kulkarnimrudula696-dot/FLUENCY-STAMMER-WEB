import sys, os
sys.path.insert(0, os.path.abspath('.'))
import content_data

print("=== ALL 20 YOUTUBE VIDEOS IN DATASET ===")
seen_yids = set()
yid_items = []
for v in content_data.VIDEO_PRACTICE_ITEMS:
    yid = v.get('youtube_id')
    if yid not in seen_yids:
        seen_yids.add(yid)
        yid_items.append(v)

for idx, v in enumerate(yid_items):
    print(f"{idx+1}. YT ID: {v.get('youtube_id')} | Title: {v.get('title')}")

print("\n=== ALL 20 UNSPLASH IMAGES IN DATASET ===")
seen_imgs = set()
img_items = []
for im in content_data.IMAGE_PRACTICE_ITEMS:
    url = im.get('image_url')
    if url not in seen_imgs:
        seen_imgs.add(url)
        img_items.append(im)

for idx, im in enumerate(img_items):
    print(f"{idx+1}. Image URL: {im.get('image_url')}")
    print(f"   Sample Title: {im.get('title')}")
