import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from speech_analyzer import analyze_speech_data, compare_reading_paragraph
import content_data

print("=== 1. TESTING LOCALIZED PASSAGE GENERATION ===")
test_languages = ['Hindi', 'Marathi', 'Spanish', 'French', 'German', 'Japanese', 'Chinese', 'English']

with app.test_client() as client:
    for lang in test_languages:
        res = client.get(f'/api/content/reading?language={lang}&age_group=18-23&length_type=short&difficulty=easy')
        assert res.status_code == 200, f"Failed for {lang}: {res.status_code}"
        data = res.get_json()
        assert data['count'] > 0, f"No passages for {lang}"
        item = data['items'][0]
        print(f"[{lang}] Count: {data['count']} | Title: {item['title'][:30]} | Sample: {item['text'][:45]}...")

print("\n=== 2. TESTING SPEECH MATCHING ON HINDI ===")
expected_hi = "जब हम धीरे बोलते हैं तो आवाज़ में सहजता आती है।"
spoken_hi = "जब हम बोलते हैं धीरे तो आवाज़ में सहजता आती है।"

res_matching = compare_reading_paragraph(expected_hi, spoken_hi)
print("Hindi match %:", res_matching['match_pct'])
print("Hindi wrong order:", res_matching['wrong_order'])
print("Hindi correct:", res_matching['correct'])
print("Hindi summary:", res_matching['summary'])

assert 'धीरे' in res_matching['wrong_order'], "Expected 'धीरे' to be detected as wrong word order"
assert len(res_matching['correct']) > 0, "Expected correct words to be detected"

print("\n=== 3. TESTING SPEECH MATCHING ON MARATHI ===")
expected_mr = "शांतपणे बोलणे हा दुर्बलपणा नसून आत्मविश्वासाचे लक्षण आहे."
spoken_mr = "शांतपणे बोलणे हा बोलणे हा आत्मविश्वासाचे लक्षण आहे."

res_mr = compare_reading_paragraph(expected_mr, spoken_mr)
print("Marathi match %:", res_mr['match_pct'])
print("Marathi repeated:", res_mr['repeated'])
print("Marathi replaced:", res_mr['replaced'])
print("Marathi missing:", res_mr['missing'])
print("Marathi summary:", res_mr['summary'])

assert len(res_mr['replaced']) == 2, "Expected 2 substitutions (replaced words) in Marathi"
assert len(res_mr['repeated']) > 0, "Expected repetition in Marathi"

print("\n=== 4. TESTING ANALYZE SPEECH DATA WITH WRONG WORD ORDER ===")
feedback = analyze_speech_data(
    transcript=spoken_hi,
    audio_duration_seconds=6.0,
    prompt_text=expected_hi,
    mode='reading'
)
pm = feedback['paragraph_match']
print("Paragraph match percentage:", pm['match_percentage'])
print("Missing words count:", len(pm['missing_words']))
print("Wrong order words:", pm['wrong_order_words'])
print("Metrics wrong_order_words_count:", feedback['metrics']['wrong_order_words_count'])
assert feedback['metrics']['wrong_order_words_count'] == len(pm['wrong_order_words'])

print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
