import urllib.request
import json

test_list = [
    ("69Q_3VQ07vA", "The ABCs of Stuttering"),
    ("Po-WMo8vXRY", "Stuttering: For Kids By Kids"),
    ("Mn2iAfkqews", "Stuttering: For Kids, By Kids 2.0"),
    ("7SUcxAjG2GI", "Stuttering: Straight Talk for Teens"),
    ("ix65403ruKI", "Stuttering: Straight Talk for Teachers"),
    ("wTpckAufNDE", "7 Tips for Talking with the Child Who Stutters"),
    ("u2_mgt87g1Y", "Stuttering and Your Child: Help for Parents"),
    ("03yQQo_LUf0", "Kids Who Stutter: Parents Speak"),
    ("_tE_Smzf_xU", "If You Stutter: Advice for Adults"),
    ("MXh9OWIIU5g", "Stuttering 101"),
    ("Jm3191t6a_U", "Stuttering, Vulnerability, and Intimacy / Constantino"),
    ("Vl8dF2y7YhY", "Helping Children Change Their Thoughts & Feelings / Sisskin"),
    ("OJ2o3OF_XP0", "Help Children Overcome Bullying / Murphy"),
    ("QmepajAKavs", "My Beautiful Stutter / SAY"),
    ("i9_9pWk9H34", "Rational Emotive Behavior Therapy / Hollister"),
    ("9LP54UCtrrc", "The Role of Acceptance, Commitment and Mindfulness in Stuttering Therapy"),
    ("JDcpe4lOWD8", "Voluntary Stuttering / Donaher"),
    ("DJxkoYWWX_o", "ADHD & Children Who Stutter / Donaher"),
    ("S0T00uF30sY", "Working with Preschoolers Who Stutter / Chmela"),
    ("OjuD8RBNDz4", "Avoidance Reduction Therapy / Sisskin")
]

valid_count = 0
for vid_id, label in test_list:
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid_id}&format=json"
    try:
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            title = data.get('title')
            author = data.get('author_name')
            thumb = data.get('thumbnail_url')
            print(f"[VALID {valid_count+1}/20] {vid_id} -> '{title}' ({author}) | thumb='{thumb}'")
            valid_count += 1
    except Exception as e:
        print(f"[FAIL] {vid_id} ({label}) -> {e}")

print(f"\nTOTAL VALID: {valid_count} / {len(test_list)}")
