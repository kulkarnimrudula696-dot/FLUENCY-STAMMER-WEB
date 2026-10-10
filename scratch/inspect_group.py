import sys, os
sys.path.insert(0, os.path.abspath('.'))
import content_data

vids = [v for v in content_data.VIDEO_PRACTICE_ITEMS if v.get('age_group') == '18-25']
print(f"Total 18-25 videos: {len(vids)}")
for diff in ['Easy', 'Medium', 'Hard']:
    diff_vids = [v for v in vids if v.get('difficulty') == diff]
    print(f"  {diff}: {len(diff_vids)} items")
    for idx, v in enumerate(diff_vids):
        print(f"    [{idx+1}] ID: {v.get('id')} | YT: {v.get('youtube_id')} | Title: {v.get('title')}")

imgs = [im for im in content_data.IMAGE_PRACTICE_ITEMS if im.get('age_group') == '18-25']
print(f"\nTotal 18-25 images: {len(imgs)}")
for diff in ['Easy', 'Medium', 'Hard']:
    diff_imgs = [im for im in imgs if im.get('difficulty') == diff]
    print(f"  {diff}: {len(diff_imgs)} items")
    for idx, im in enumerate(diff_imgs):
        photo_id = im.get('image_url').split('photo-')[-1].split('?')[0]
        print(f"    [{idx+1}] ID: {im.get('id')} | Photo: {photo_id} | Title: {im.get('title')}")
