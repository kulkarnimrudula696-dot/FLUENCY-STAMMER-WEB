import json

with open('scratch/unified_media.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

imgs = data['images']
vids = data['videos']

print(f"Total Images: {len(imgs)}, Total Videos: {len(vids)}")

print("\n--- SAMPLE IMAGE 1 (Park) ---")
i1 = imgs[0]
print(f"ID: {i1['id']} | Title: {i1['title']}")
print(f"Media: {i1['media']}")
print(f"Prompt: {i1['prompt']}")
print(f"Questions: {i1['guidingQuestions']}")
print(f"Vocabulary: {i1['vocabulary']}")

print("\n--- SAMPLE IMAGE 8 (Kitchen Cooking) ---")
i8 = imgs[7]
print(f"ID: {i8['id']} | Title: {i8['title']}")
print(f"Media: {i8['media']}")
print(f"Prompt: {i8['prompt']}")
print(f"Questions: {i8['guidingQuestions']}")
print(f"Vocabulary: {i8['vocabulary']}")

print("\n--- SAMPLE VIDEO 1 (For the Birds) ---")
v1 = vids[0]
print(f"ID: {v1['id']} | Title: {v1['title']}")
print(f"YT ID: {v1['youtube_id']} | Media: {v1['media']}")
print(f"Prompt: {v1['prompt']}")
print(f"Questions: {v1['guidingQuestions']}")
print(f"Vocabulary: {v1['vocabulary']}")

print("\n--- SAMPLE VIDEO 8 (The Present) ---")
v8 = vids[7]
print(f"ID: {v8['id']} | Title: {v8['title']}")
print(f"YT ID: {v8['youtube_id']} | Media: {v8['media']}")
print(f"Prompt: {v8['prompt']}")
print(f"Questions: {v8['guidingQuestions']}")
print(f"Vocabulary: {v8['vocabulary']}")
