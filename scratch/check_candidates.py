import urllib.request
import json

candidate_ids = [
    ("R953Y77eP1Y", "The ABCs of Stuttering"),
    ("zeOO3nP6Emw", "Our 75th Anniversary / Stuttering Foundation"),
    ("Mn2iAfkqews", "Stuttering: For Kids, By Kids 2.0"),
    ("7SUcxAjG2GI", "Stuttering: Straight Talk for Teens"),
    ("ix65403ruKI", "Stuttering: Straight Talk for Teachers"),
    ("wTpckAufNDE", "7 Tips for Talking with the Child Who Stutters"),
    ("u2_mgt87g1Y", "Stuttering and Your Child: Help for Parents"),
    ("03yQQo_LUf0", "Kids Who Stutter: Parents Speak"),
    ("MXh9OWIIU5g", "Stuttering 101"),
    ("09qEzfVt_bk", "Stuttering: Basic Clinical Skills"),
    ("s0n00sZgRyo", "Advice for Teachers / Classroom Strategies"),
    ("F0sD94Oq5tY", "Wait Wait Wait / Advice from Young People"),
    ("wAA4hvGIlZY", "Supporting Children Who Stammer in School"),
    ("b0V-m8mU9L8", "What is Stammering? Michael Palin Centre"),
    ("iFm2yK180kE", "Parents Experiences of Therapy"),
    ("R96yS371C8g", "Building Confidence in Stammering"),
    ("Gk7M4jO1uXw", "Therapy Techniques"),
    ("q62X1J5_x3E", "Living with Stammering"),
]

print("Checking candidate video IDs...")
for vid_id, note in candidate_ids:
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid_id}&format=json"
    try:
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[VALID] {vid_id} -> '{data.get('title')}' ({note}) | author='{data.get('author_name')}'")
    except Exception as e:
        print(f"[INVALID] {vid_id} -> {e} ({note})")
