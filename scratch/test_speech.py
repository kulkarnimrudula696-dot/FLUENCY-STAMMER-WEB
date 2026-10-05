import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speech_analyzer import analyze_speech_data, compare_reading_paragraph

exp_hi = 'जब हम जल्दबाज़ी में बोलते हैं, तो सांस रुक जाती है।'
spk_hi = 'जब हम बोलते हैं जल्दबाज़ी में सांस रुक जाती है।'
res_hi = compare_reading_paragraph(exp_hi, spk_hi)
print('Hindi match pct:', res_hi['match_pct'])
print('Hindi wrong order:', res_hi['wrong_order'])
print('Hindi correct:', res_hi['correct'])
print('Hindi missing:', res_hi['missing'])
print('Hindi extra:', res_hi['extra'])

full_analysis = analyze_speech_data(transcript=spk_hi, prompt_text=exp_hi, audio_duration_seconds=5.0, mode='reading')
print('Practice score:', full_analysis['practice_score'])
print('Payload wrong order words:', full_analysis['paragraph_match']['wrong_order_words'])
print('Summary:', full_analysis['paragraph_match']['summary'])
