import re
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

with open('static/js/video_mode.js', 'r', encoding='utf-8') as f:
    text = f.read()

vids = re.findall(r'"id":\s*"(vid_[^"]+)"', text)
imgs = re.findall(r'"id":\s*"(img_[^"]+)"', text)
print(f"video_mode.js IDs: vids={len(vids)}, imgs={len(imgs)}")

import content_data
print(f"content_data.py items: vids={len(content_data.VIDEO_PRACTICE_ITEMS)}, imgs={len(content_data.IMAGE_PRACTICE_ITEMS)}")

for ag in ['6-11', '12-17', '18-23', '24-30', '31-40']:
    v_ag = content_data.get_videos_for_age_and_diff(ag, 'all')
    i_ag = content_data.get_images_for_age_and_diff(ag, 'all')
    print(f"Age group {ag}: {len(v_ag)} videos, {len(i_ag)} images")
