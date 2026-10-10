generator_code = '''
AGE_GROUPS = ['6-9', '10-12', '13-17', '18-25', '26-32', '33-40']
DIFFICULTIES = ['Easy', 'Medium', 'Hard']

all_images = []
for ag in AGE_GROUPS:
    ag_tag = ag.replace('-', '_')
    for diff in DIFFICULTIES:
        diff_tag = diff.lower()
        for item in IMAGE_CATALOG:
            idx = item['index']
            tier = item['tiers'][diff]
            item_id = f"img_{ag_tag}_{diff_tag}_{idx}"
            img_obj = {
                "id": item_id,
                "media": item["image_url"],
                "mediaType": "image",
                "media_type": "image",
                "title": tier["title"],
                "prompt": tier["prompt"],
                "clue": tier["prompt"],
                "description": tier["description"],
                "instruction": tier["description"],
                "description_prompt": tier["description"],
                "guidingQuestions": tier["guidingQuestions"],
                "guiding_questions": tier["guidingQuestions"],
                "vocabulary": tier["vocabulary"],
                "suggested_keywords": tier["vocabulary"],
                "age_group": ag,
                "category": "Visual Speaking Practice",
                "difficulty": diff,
                "difficulty_tag": diff,
                "length_type": "medium",
                "duration": "Visual Scene",
                "duration_label": "Visual Scene",
                "image_url": item["image_url"],
                "thumbnail": item["thumbnail"]
            }
            all_images.append(img_obj)

all_videos = []
for ag in AGE_GROUPS:
    ag_tag = ag.replace('-', '_')
    for diff in DIFFICULTIES:
        diff_tag = diff.lower()
        for item in VIDEO_CATALOG:
            idx = item['index']
            tier = item['tiers'][diff]
            item_id = f"vid_{ag_tag}_{diff_tag}_{idx}"
            dur_str = item['durations'].get(diff, '4 min')
            dur_min = int(dur_str.split()[0]) if dur_str and dur_str.split()[0].isdigit() else 4
            dur_sec = dur_min * 60
            vid_obj = {
                "id": item_id,
                "media": item["youtubeEmbedUrl"],
                "mediaType": "video",
                "media_type": "video",
                "title": tier["title"],
                "prompt": tier["prompt"],
                "clue": tier["prompt"],
                "description": tier["description"],
                "instruction": tier["description"],
                "description_prompt": tier["description"],
                "guidingQuestions": tier["guidingQuestions"],
                "guiding_questions": tier["guidingQuestions"],
                "vocabulary": tier["vocabulary"],
                "suggested_keywords": tier["vocabulary"],
                "age_group": ag,
                "category": "Video Speaking Practice",
                "difficulty": diff,
                "difficulty_tag": diff,
                "duration": dur_str,
                "duration_label": f"{dur_str} practice",
                "duration_seconds": dur_sec,
                "youtube_id": item["youtube_id"],
                "youtubeEmbedUrl": item["youtubeEmbedUrl"],
                "embed_url": item["embed_url"],
                "thumbnail": f"https://img.youtube.com/vi/{item['youtube_id']}/hqdefault.jpg",
                "youtube_search_url": f"https://www.youtube.com/results?search_query={tier['title'].replace(' ', '+')}"
            }
            all_videos.append(vid_obj)

print(f"Generated {len(all_images)} unified images and {len(all_videos)} unified videos.")

# Save to scratch/unified_media.json
with open('scratch/unified_media.json', 'w', encoding='utf-8') as out_f:
    json.dump({'images': all_images, 'videos': all_videos}, out_f, indent=2, ensure_ascii=False)
print("Saved scratch/unified_media.json successfully.")
'''

with open('scratch/build_unified_media.py', 'a', encoding='utf-8') as f:
    f.write('\n' + generator_code)
print("Appended generator code to build_unified_media.py")
