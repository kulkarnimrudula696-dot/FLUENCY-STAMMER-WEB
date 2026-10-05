"""
FLUENCY Speech Analysis Engine
Genuinely useful, honest, supportive, calm, and actionable speech analysis.

Evaluates actual recorded speech and transcription:
1. Exact Paragraph Comparison & Alignment (Reading Mode):
   - Paragraph Match %
   - Matched Words Count vs Total Expected
   - Missing Words (words from paragraph not spoken)
   - Extra / Unrelated Words (extraneous speech added by user)
   - Replaced / Mismatched Words (substitutions)
   - Repeated Words / Phrases (stutters & repetitions)
2. Speaking Time (duration in seconds/minutes)
3. Words Spoken (exact word count)
4. Speaking Rate (words per minute)
5. Long Pauses (pauses >2.0s beyond natural breathing)
6. Repetitions (repeated words, repeated syllables/sounds, restarted sentences)
7. Filler Words (count & breakdown of 'um', 'uh', 'like', 'you know', etc.)
"""

import re
import math
import os
import json
import logging
import difflib

logger = logging.getLogger(__name__)

COMMON_FILLERS = [
    "um", "uh", "er", "ah", "like", "you know", "actually", "basically",
    "literally", "i mean", "sort of", "kind of", "right", "so yeah", "honestly"
]

def format_duration(seconds):
    """Format duration into readable string: '18s' or '1m 14s'"""
    seconds = max(0, int(round(seconds)))
    if seconds < 60:
        return f"{seconds}s"
    mins = seconds // 60
    rem = seconds % 60
    return f"{mins}m {rem}s" if rem > 0 else f"{mins}m"


def clean_tokens(text):
    """Extract lowercase words supporting Unicode letters, hyphens, and apostrophes."""
    if not text:
        return []
    return [w.lower() for w in re.findall(r"[\w'-]+", text, re.UNICODE) if w.strip()]


def compare_reading_paragraph(expected_text, spoken_text):
    """
    Strict Sequence-Aligned Paragraph Comparison for Reading Mode.
    Compares the ACTUAL speech transcript with the EXACT displayed paragraph.
    
    Identifies:
    - Matched words in correct sequence
    - Missing words (skipped from paragraph)
    - Extra words (unrelated/extraneous words added by user)
    - Replaced/Mismatched words (substitutions)
    - Repeated words / phrases (stutters or repetitions)
    - Paragraph Match % (penalizing missing words, extra speech, and substitutions)
    """
    expected_words = clean_tokens(expected_text)
    spoken_words = clean_tokens(spoken_text)

    if not expected_words:
        return {
            "match_pct": 100.0,
            "matched_count": len(spoken_words),
            "total_expected": len(spoken_words),
            "missing": [],
            "extra": [],
            "replaced": [],
            "repeated": [],
            "is_reading_mode": False,
            "summary": "Free speech practice (No fixed paragraph comparison)."
        }

    if not spoken_words:
        return {
            "match_pct": 0.0,
            "matched_count": 0,
            "total_expected": len(expected_words),
            "missing": expected_words,
            "extra": [],
            "replaced": [],
            "repeated": [],
            "is_reading_mode": True,
            "summary": "No speech detected. All paragraph words were missed."
        }

    matcher = difflib.SequenceMatcher(None, expected_words, spoken_words)
    opcodes = matcher.get_opcodes()

    matched_words = []
    missing_words = []
    extra_words = []
    replaced_words = []

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            matched_words.extend(expected_words[i1:i2])
        elif tag == 'delete':
            # In expected paragraph but missing from spoken speech
            missing_words.extend(expected_words[i1:i2])
        elif tag == 'insert':
            # In speech but NOT in expected paragraph (extra/unrelated)
            extra_words.extend(spoken_words[j1:j2])
        elif tag == 'replace':
            exp_chunk = expected_words[i1:i2]
            spk_chunk = spoken_words[j1:j2]
            min_len = min(len(exp_chunk), len(spk_chunk))
            for k in range(min_len):
                replaced_words.append({"expected": exp_chunk[k], "spoken": spk_chunk[k]})
            if len(exp_chunk) > min_len:
                missing_words.extend(exp_chunk[min_len:])
            if len(spk_chunk) > min_len:
                extra_words.extend(spk_chunk[min_len:])

    # Detect repeated words or phrases in the spoken transcript
    repeated_items = []
    for idx in range(len(spoken_words) - 1):
        if spoken_words[idx] == spoken_words[idx + 1]:
            rep_str = f"{spoken_words[idx]} {spoken_words[idx]}"
            if rep_str not in repeated_items:
                repeated_items.append(rep_str)

    for idx in range(len(spoken_words) - 3):
        p1 = f"{spoken_words[idx]} {spoken_words[idx+1]}"
        p2 = f"{spoken_words[idx+2]} {spoken_words[idx+3]}"
        if p1 == p2 and p1 not in repeated_items:
            repeated_items.append(p1)

    n_exp = len(expected_words)
    n_match = len(matched_words)
    raw_accuracy = (n_match / max(n_exp, 1)) * 100.0

    # Penalties for extraneous speech and substitutions
    # Unrelated/extra speech penalty:
    extra_penalty = (len(extra_words) / max(n_exp, 1)) * 50.0
    # Replaced words penalty:
    replace_penalty = (len(replaced_words) / max(n_exp, 1)) * 35.0

    match_pct = max(0.0, min(100.0, round(raw_accuracy - extra_penalty - replace_penalty, 1)))

    # Summary
    if n_match == n_exp and len(extra_words) == 0 and len(replaced_words) == 0:
        summary = "100% Exact Match: You read the entire paragraph accurately."
    else:
        parts = [f"{n_match}/{n_exp} words matched"]
        if missing_words:
            parts.append(f"{len(missing_words)} missing")
        if extra_words:
            parts.append(f"{len(extra_words)} extra/unrelated")
        if replaced_words:
            parts.append(f"{len(replaced_words)} replaced")
        if repeated_items:
            parts.append(f"{len(repeated_items)} repeated")
        summary = " · ".join(parts)

    return {
        "match_pct": match_pct,
        "matched_count": n_match,
        "total_expected": n_exp,
        "missing": missing_words,
        "extra": extra_words,
        "replaced": replaced_words,
        "repeated": repeated_items,
        "is_reading_mode": True,
        "summary": summary
    }


def detect_filler_words(transcript):
    """Detect single and multi-word filler sounds from actual transcript."""
    detected = []
    total_count = 0
    lower_text = transcript.lower()
    words = re.findall(r"\b[\w'-]+\b", lower_text)

    # Multi-word fillers first
    for filler in COMMON_FILLERS:
        if " " in filler:
            matches = len(re.findall(r'\b' + re.escape(filler) + r'\b', lower_text))
            if matches > 0:
                detected.append({"word": filler, "count": matches, "type": "phrase"})
                total_count += matches

    # Single-word fillers
    for filler in COMMON_FILLERS:
        if " " not in filler:
            matches = words.count(filler)
            if matches > 0:
                detected.append({"word": filler, "count": matches, "type": "word"})
                total_count += matches

    return detected, total_count


def detect_repetitions_and_restarts(transcript, prompt_text=""):
    """
    Detect repeated words, repeated syllables/sounds, and restarted phrases.
    Only flags actual disfluency repetitions that are NOT part of the printed prompt text.
    """
    lower_text = transcript.lower()
    lower_prompt = (prompt_text or "").lower()
    words = re.findall(r"\b[\w'-]+\b", lower_text)
    
    repeated_words_list = []
    syllable_stutters = []
    restarted_phrases = []

    # 1. Immediate word repetitions (e.g. "I I", "the the", "we we")
    for i in range(len(words) - 1):
        if words[i] == words[i+1] and len(words[i]) > 0:
            rep_str = f"{words[i]} {words[i]}"
            if rep_str not in lower_prompt:
                repeated_words_list.append(rep_str)

    # 2. Syllable/sound stutters (e.g. "b-b-because", "wh-when", "s-s-so", "p-practice")
    stutter_matches = re.findall(r'\b([a-zA-Z]{1,3})[-]+([a-zA-Z]+)\b', lower_text)
    for prefix, full_word in stutter_matches:
        if full_word.startswith(prefix.lower()):
            syllable_stutters.append(f"{prefix}-{full_word}")

    # 3. Restarted phrases / false starts (e.g. "I went to... I went to the store")
    for i in range(len(words) - 3):
        two_words = f"{words[i]} {words[i+1]}"
        subsequent = " ".join(words[i+2:i+7])
        if two_words in subsequent:
            if two_words not in lower_prompt or lower_prompt.count(two_words) <= 1:
                restarted_phrases.append(two_words)

    all_repetitions = list(set(repeated_words_list + syllable_stutters + restarted_phrases))
    total_count = len(repeated_words_list) + len(syllable_stutters) + len(restarted_phrases)

    return all_repetitions, total_count, repeated_words_list, syllable_stutters, restarted_phrases


def detect_long_pauses(transcript, duration_seconds, word_count):
    """
    Calculate natural breathing pauses vs unusually long pauses (>2.0s).
    Based on standard speech production pacing (~2.2 words/sec) and punctuation marks.
    """
    if word_count == 0 or duration_seconds <= 0:
        return 0, 0

    expected_speaking_time = word_count / 2.17
    total_silence_time = max(0.0, duration_seconds - expected_speaking_time)

    punctuation_count = len(re.findall(r'[.,!?;—]', transcript))
    healthy_pause_time = punctuation_count * 0.85

    excess_pause_time = max(0.0, total_silence_time - healthy_pause_time)
    long_pauses_count = int(excess_pause_time // 2.0)
    natural_pauses_count = max(punctuation_count, int(min(total_silence_time, healthy_pause_time) / 0.85))

    return long_pauses_count, natural_pauses_count


def extract_difficult_words(transcript, prompt_text, repetitions_list):
    """
    Identify actual words where user appeared to struggle.
    NEVER invent difficult words. Only mention words from the user's transcript/prompt.
    """
    words = re.findall(r"\b[\w'-]+\b", transcript.lower())
    struggled_words = set()

    for rep in repetitions_list:
        rep_tokens = re.findall(r"\b[a-zA-Z]+\b", rep)
        for tok in rep_tokens:
            if len(tok) >= 4 and tok not in COMMON_FILLERS:
                struggled_words.add(tok)

    if prompt_text:
        prompt_words = re.findall(r"\b[\w'-]+\b", prompt_text.lower())
        for pw in prompt_words:
            if len(pw) >= 8 and pw not in words and pw not in struggled_words:
                struggled_words.add(pw)

    return list(struggled_words)[:3]


def analyze_speech_data(transcript, audio_duration_seconds=0, prompt_text="", user_practice_age=21, custom_api_key=None, mode="reading"):
    """
    Main entry point for speech analysis.
    Takes transcript, actual duration in seconds, prompt text, and practice mode.
    Performs strict sequence alignment for Reading and Tongue Twister modes.
    """
    transcript = (transcript or "").strip()
    words = clean_tokens(transcript)
    word_count = len(words)
    audio_duration_seconds = float(audio_duration_seconds or 0)
    is_twister_mode = str(mode).lower() in ['twister', 'tongue_twister', 'tongue-twister']

    if audio_duration_seconds <= 0 and word_count > 0:
        audio_duration_seconds = max(round(word_count / 2.1, 1), 3.0)

    duration_minutes = audio_duration_seconds / 60.0 if audio_duration_seconds > 0 else 0.0

    # Paragraph / Tongue Twister Matching
    has_expected_prompt = bool(prompt_text and len(clean_tokens(prompt_text)) >= 1)
    paragraph_match_result = compare_reading_paragraph(prompt_text, transcript) if has_expected_prompt else None

    # Handle zero input / silence
    if word_count == 0:
        item_label = "tongue twister" if is_twister_mode else "paragraph"
        match_info = {
            "match_percentage": 0.0,
            "matched_words_count": 0,
            "total_expected_words": len(clean_tokens(prompt_text)) if prompt_text else 0,
            "missing_words": clean_tokens(prompt_text) if prompt_text else [],
            "extra_words": [],
            "replaced_words": [],
            "repeated_words": [],
            "is_reading_mode": has_expected_prompt,
            "is_twister_mode": is_twister_mode,
            "mode_label": "Tongue Twister" if is_twister_mode else "Reading Mode",
            "summary": f"No speech recorded. 0% {item_label} match." if has_expected_prompt else "No speech detected."
        }

        return {
            "metrics": {
                "speaking_time_seconds": round(audio_duration_seconds, 1),
                "speaking_time_display": format_duration(audio_duration_seconds),
                "words_spoken": 0,
                "words_spoken_display": "0 words",
                "speaking_rate_wpm": 0.0,
                "speaking_rate_display": "0 WPM",
                "pace_status": "No speech detected",
                "long_pauses": 0,
                "long_pauses_display": "0 long pauses",
                "repetitions": 0,
                "repetitions_display": "0 repetitions",
                "repetitions_list": [],
                "filler_words": 0,
                "filler_words_display": "0 fillers",
                "fillers_list": [],
                "practice_score": 0,
                "practice_score_display": "0/100",
                "paragraph_match_pct": 0.0,
                "missing_words_count": len(match_info["missing_words"]),
                "extra_words_count": 0,
                "replaced_words_count": 0,
                "repeated_words_count": 0,
                "wpm": 0.0,
                "word_count": 0,
                "duration_seconds": round(audio_duration_seconds, 1),
                "filler_count": 0,
                "pauses_count": 0,
                "long_pauses_count": 0,
                "repetitions_count": 0,
                "clarity_score": 0.0,
                "sentence_completion_pct": 0.0,
                "consistency_score": 0.0
            },
            "practice_score": 0,
            "practice_score_display": "0/100",
            "practice_score_focus": f"No speech audio detected. Read the {item_label} aloud into your microphone.",
            "pattern_noticed": "No audio signal was captured. Make sure your microphone is connected and allowed.",
            "your_speech_feedback": {
                "what_went_well": ["You initiated the recording session."],
                "what_needs_improvement": ["The microphone did not register spoken words during this attempt."],
                "main_difficulty_location": "Microphone input / speech detection.",
                "speech_pattern_noticed": "Audio input was silent.",
                "what_to_practise_next": f"Check microphone settings, speak clearly at a conversational volume, and read the displayed {item_label}."
            },
            "what_went_well": ["You initiated the practice recording session."],
            "needs_improvement": [{
                "issue": "No Speech Detected",
                "why_it_matters": "The microphone did not register spoken words during this attempt.",
                "how_to_fix": f"Speak at a normal conversational volume and read the {item_label}."
            }],
            "paragraph_match": match_info,
            "difficult_words": [],
            "difficult_words_practice": "",
            "next_practice": {
                "title": "Next Practice",
                "instruction": "Repeat these 2 sentences three times at your natural speaking pace:",
                "sentences": [
                    "Hello, my voice is calm, clear, and steady today.",
                    "Speaking with gentle pauses helps me share every thought with ease."
                ],
                "mode": mode if is_twister_mode else "reading",
                "reason": "Reading aloud is the best way to develop agile speech motor control."
            },
            "transcript": "",
            "ai_service_configured": bool(custom_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")),
            "disclaimer": "FLUENCY speech analysis provides educational acoustic and behavioral speaking feedback. It does not provide medical diagnoses."
        }

    # -------------------------------------------------------------------------
    # 1. ACOUSTIC METRICS CALCULATION
    # -------------------------------------------------------------------------
    speaking_time_display = format_duration(audio_duration_seconds)
    words_spoken_display = f"{word_count} words"

    wpm = round((word_count / duration_minutes), 1) if duration_minutes > 0 else 0.0
    speaking_rate_display = f"{wpm} WPM"

    if 110 <= wpm <= 155:
        pace_status = "Optimal Conversational Pace"
        pace_eval = "optimal"
    elif 85 <= wpm < 110:
        pace_status = "Calm & Deliberate Pace (Controlled Flow)"
        pace_eval = "deliberate"
    elif 65 <= wpm < 85:
        pace_status = "Slow Pacing (Focus on Phrase Linking)"
        pace_eval = "slow"
    elif 155 < wpm <= 175:
        pace_status = "Brisk Pace (Slightly Fast)"
        pace_eval = "brisk"
    elif wpm > 175:
        pace_status = "Very Fast / Rushed (Syllable Collisions)"
        pace_eval = "fast"
    else:
        pace_status = "Very Slow / Extended Hesitations"
        pace_eval = "very_slow"

    # Pauses, repetitions, fillers
    long_pauses_count, natural_pauses_count = detect_long_pauses(transcript, audio_duration_seconds, word_count)
    long_pauses_display = f"{long_pauses_count} long pause{'s' if long_pauses_count != 1 else ''}"

    all_repetitions, repetition_count, repeated_words_list, syllable_stutters, restarted_phrases = detect_repetitions_and_restarts(transcript, prompt_text)
    repetitions_display = f"{repetition_count} repetition{'s' if repetition_count != 1 else ''}"

    detected_fillers, filler_count = detect_filler_words(transcript)
    filler_words_display = f"{filler_count} filler word{'s' if filler_count != 1 else ''}"

    # -------------------------------------------------------------------------
    # 2. PRACTICE SCORE & READING ACCURACY DEDUCTIONS
    # -------------------------------------------------------------------------
    base_score = 100.0
    repetition_deduction = min(36.0, repetition_count * 12.0)
    pause_deduction = min(30.0, long_pauses_count * 10.0)
    filler_deduction = min(24.0, filler_count * 6.0)

    pace_deduction = 0.0
    if pace_eval in ["fast", "very_slow"]:
        pace_deduction = 14.0
    elif pace_eval in ["brisk", "slow"]:
        pace_deduction = 6.0

    trailing_off = transcript.endswith("...") or (word_count > 3 and transcript[-1] not in ".!?\"'")
    trailing_deduction = 8.0 if trailing_off else 0.0

    total_deductions = repetition_deduction + pause_deduction + filler_deduction + pace_deduction + trailing_deduction
    fluency_score = max(15.0, min(100.0, base_score - total_deductions))

    # Strict score calculation for Reading Mode vs Free Speech
    if paragraph_match_result and paragraph_match_result.get("is_reading_mode"):
        match_pct = paragraph_match_result["match_pct"]
        if match_pct <= 0:
            # Spoke completely unrelated speech
            practice_score = 10
        else:
            # Weighted: 70% paragraph reading accuracy + 30% fluency flow
            calculated_score = (match_pct * 0.70) + (fluency_score * 0.30)
            practice_score = int(round(max(10.0, min(100.0, calculated_score))))
    else:
        practice_score = int(round(fluency_score))

    practice_score_display = f"{practice_score}/100"

    # Focus Areas
    focus_areas = []
    if paragraph_match_result and paragraph_match_result.get("is_reading_mode"):
        if len(paragraph_match_result["extra"]) > 0:
            focus_areas.append("reading strictly the words in the paragraph without extraneous speech")
        if len(paragraph_match_result["missing"]) > 0:
            focus_areas.append("tracking every word to avoid skipping phrases")
        if len(paragraph_match_result["replaced"]) > 0:
            focus_areas.append("accurate word pronunciation matching the text")
    if repetition_count > 0:
        focus_areas.append("smoother sentence starts without phrase restarts")
    if filler_count > 0:
        focus_areas.append("replacing filler sounds with brief silent pauses")
    if long_pauses_count > 0:
        focus_areas.append("linking short 3–4 word phrases smoothly")

    if focus_areas:
        focus_text = " and ".join(focus_areas[:2])
        practice_score_focus = f"Your current focus: {focus_text}."
    else:
        practice_score_focus = "Your current focus: maintaining this smooth, steady conversational rhythm."

    # -------------------------------------------------------------------------
    # 3. PATTERN I NOTICED
    # -------------------------------------------------------------------------
    if paragraph_match_result and paragraph_match_result.get("is_reading_mode"):
        p_extra = paragraph_match_result["extra"]
        p_missing = paragraph_match_result["missing"]
        p_replaced = paragraph_match_result["replaced"]
        p_match = paragraph_match_result["match_pct"]
        item_lbl = "tongue twister" if is_twister_mode else "paragraph"

        if p_match == 100.0:
            pattern_noticed = f"Flawless articulation! You read every word of the {item_lbl} accurately in exact sequence with steady motor control." if is_twister_mode else "You read every word of the paragraph accurately in exact sequence with steady articulation."
        elif len(p_extra) > 0 and p_match >= 40:
            sample_extra = ", ".join([f"'{w}'" for w in p_extra[:4]])
            pattern_noticed = f"You read the {item_lbl} but added extra/unrelated speech ({sample_extra}) that was not in the text."
        elif len(p_extra) > (paragraph_match_result["matched_count"] * 2) and p_match < 30:
            pattern_noticed = f"The recorded speech was largely unrelated to the displayed {item_lbl}."
        elif len(p_missing) >= 3:
            sample_miss = ", ".join([f"'{w}'" for w in p_missing[:3]])
            pattern_noticed = f"You skipped words from the {item_lbl} ({sample_miss})."
        elif len(p_replaced) > 0:
            rep_ex = p_replaced[0]
            pattern_noticed = f"Phoneme slip detected: you said '{rep_ex['spoken']}' instead of '{rep_ex['expected']}'."
        elif repetition_count >= 2:
            pattern_noticed = "You tended to repeat initial words when beginning new sentences."
        elif filler_count >= 3:
            pattern_noticed = f"You used '{detected_fillers[0]['word']}' as a bridge between phrases."
        else:
            pattern_noticed = f"You maintained a consistent reading pace with minor phrase variations."
    else:
        if repetition_count >= 2 and filler_count >= 2:
            pattern_noticed = "You tended to repeat initial words and insert filler sounds when formulating the next phrase."
        elif repetition_count >= 2:
            pattern_noticed = "You tended to restart sentences and repeat initial words when beginning a new thought."
        elif filler_count >= 3:
            pattern_noticed = f"You used '{detected_fillers[0]['word']}' as a verbal bridge between ideas instead of allowing a brief silent pause."
        elif long_pauses_count >= 2:
            pattern_noticed = "You had longer pauses before starting sentences, holding breath pressure before the first sound."
        elif pace_eval == "fast":
            pattern_noticed = "Your speech became noticeably faster in the middle of sentences, reducing time for syllable transitions."
        else:
            pattern_noticed = "You maintained a consistent, calm speaking rhythm with natural phrase transitions."

    # -------------------------------------------------------------------------
    # 4. STRUCTURED FEEDBACK (WHAT WENT WELL & WHAT NEEDS IMPROVEMENT)
    # -------------------------------------------------------------------------
    what_went_well = []
    what_needs_improvement = []
    needs_improvement_cards = []
    main_difficulty_location = "None — smooth delivery throughout."

    # In Reading Mode / Tongue Twister Mode, add accuracy feedback
    if paragraph_match_result and paragraph_match_result.get("is_reading_mode"):
        p_match = paragraph_match_result["match_pct"]
        p_matched_cnt = paragraph_match_result["matched_count"]
        p_total_exp = paragraph_match_result["total_expected"]
        p_missing = paragraph_match_result["missing"]
        p_extra = paragraph_match_result["extra"]
        p_replaced = paragraph_match_result["replaced"]
        p_repeated = paragraph_match_result["repeated"]
        item_lbl = "Tongue Twister" if is_twister_mode else "Reading"

        if p_match >= 90.0:
            what_went_well.append(f"High {item_lbl} Accuracy: You matched {p_matched_cnt} of {p_total_exp} words ({p_match}%) accurately.")
        elif p_matched_cnt > 0:
            what_went_well.append(f"You matched {p_matched_cnt} of {p_total_exp} words from the {item_lbl.lower()} in correct sequence.")

        if p_extra:
            extra_disp = ", ".join([f"'{w}'" for w in p_extra[:5]])
            if len(p_extra) > 5:
                extra_disp += f" (+{len(p_extra)-5} more)"
            what_needs_improvement.append(f"Extra / Unrelated Speech ({len(p_extra)} word(s) detected: {extra_disp}). Focus on speaking only the words in the {item_lbl.lower()}.")
            needs_improvement_cards.append({
                "issue": f"Extraneous Speech ({len(p_extra)} Extra Word(s))",
                "why_it_matters": f"Adding unwritten commentary or side thoughts dilutes {item_lbl.lower()} precision.",
                "how_to_fix": "Focus your gaze strictly on the prompt words and speak only what is shown without side comments."
            })
            main_difficulty_location = f"Extraneous speech added ({extra_disp})."

        if p_missing:
            miss_disp = ", ".join([f"'{w}'" for w in p_missing[:5]])
            if len(p_missing) > 5:
                miss_disp += f" (+{len(p_missing)-5} more)"
            what_needs_improvement.append(f"Skipped Words ({len(p_missing)} word(s) missed: {miss_disp}). Trace each word to ensure full phrase completion.")
            needs_improvement_cards.append({
                "issue": f"Skipped Words ({len(p_missing)} Missing)",
                "why_it_matters": "Skipping words happens when vocal speed outpaces articulatory preparation.",
                "how_to_fix": "Point or trace each word as you articulate it aloud."
            })
            if main_difficulty_location == "None — smooth delivery throughout.":
                main_difficulty_location = f"Skipped words ({miss_disp})."

        if p_replaced:
            rep_disp = ", ".join([f"'{r['expected']}' -> '{r['spoken']}'" for r in p_replaced[:3]])
            what_needs_improvement.append(f"Mismatched Words / Phoneme Slips ({len(p_replaced)} substitution(s): {rep_disp}).")
            needs_improvement_cards.append({
                "issue": f"Mismatched Words ({len(p_replaced)}x: {rep_disp})",
                "why_it_matters": "Substituting sounds happens when similar phonemes collide in rapid speech planning.",
                "how_to_fix": "Slow down your initial tempo by 30% and glide through each syllable touch point gently."
            })

    # General fluency what went well
    if natural_pauses_count >= 2 and long_pauses_count == 0:
        what_went_well.append(f"You used {natural_pauses_count} natural breathing pauses between phrases.")
    if repetition_count == 0 and word_count >= 6:
        what_went_well.append("Phrases were initiated and completed cleanly without false starts.")
    if filler_count == 0 and word_count >= 6:
        what_went_well.append("You spoke without relying on verbal fillers like 'um' or 'like'.")
    if 85 <= wpm <= 155:
        what_went_well.append(f"Your speaking rate of {wpm} WPM was in an optimal conversational tempo.")

    if not what_went_well:
        what_went_well.append(f"You completed a full {speaking_time_display} recording with {word_count} spoken words.")

    # General fluency what needs improvement
    if repetition_count > 0:
        rep_examples = ", ".join([f"'{r}'" for r in all_repetitions[:3]])
        what_needs_improvement.append(f"Repeated words ({repetition_count}x: {rep_examples}). Practise completing the phrase without restarting.")
        needs_improvement_cards.append({
            "issue": f"Phrase Restarts & Repetitions ({repetition_count}x: {rep_examples})",
            "why_it_matters": "Restarting phrases happens when physical pressure builds up before vocal cords start vibrating.",
            "how_to_fix": "Use Gentle Onset: start the first sound with a soft breath release and complete the full phrase without stopping."
        })

    if filler_count > 0:
        filler_examples = ", ".join([f"'{f['word']}' ({f['count']}x)" for f in detected_fillers[:3]])
        what_needs_improvement.append(f"Used {filler_count} filler sound(s) ({filler_examples}). Practise brief silent pauses instead.")
        needs_improvement_cards.append({
            "issue": f"Filler Sounds ({filler_count}x: {filler_examples})",
            "why_it_matters": "Filler sounds occur when keeping the voice engaged while formulating the next thought.",
            "how_to_fix": "Practise the 1-Second Silent Pause: allow complete silence while thinking instead of filling gaps with sound."
        })

    if long_pauses_count > 0:
        what_needs_improvement.append(f"Recorded {long_pauses_count} extended pause(s) (>2.0s).")
        needs_improvement_cards.append({
            "issue": f"Extended Hesitations ({long_pauses_count} pause(s) > 2.0s)",
            "why_it_matters": "Long freezes can cause tension to build in the chest and throat before speaking.",
            "how_to_fix": "Group words into short 3–4 word breath chunks and speak the first chunk on the exhale."
        })

    if not what_needs_improvement:
        what_needs_improvement.append("Your speech delivery is steady. Continue regular practice to maintain this confidence.")

    # Difficult words
    difficult_words = extract_difficult_words(transcript, prompt_text, all_repetitions)
    difficult_words_practice = ""
    if difficult_words:
        diff_str = ", ".join([f"'{w}'" for w in difficult_words])
        difficult_words_practice = f"Words to practise: {diff_str}."

    # Next Practice Sentences
    if difficult_words:
        w1 = difficult_words[0]
        w2 = difficult_words[1] if len(difficult_words) > 1 else difficult_words[0]
        practice_sentence_1 = f"I speak in a {w1} and steady voice when sharing my ideas."
        practice_sentence_2 = f"Taking a calm pause makes it {w2} to express every thought clearly."
    elif repetition_count > 0:
        practice_sentence_1 = "When I begin speaking, I let my voice glide forward into the whole sentence."
        practice_sentence_2 = "Each new phrase starts with a calm, gentle release of sound."
    elif filler_count > 0:
        practice_sentence_1 = "I pause in silent comfort before answering any question."
        practice_sentence_2 = "Silence gives my mind space to choose the exact words I want."
    else:
        practice_sentence_1 = "Calm breathing and steady pacing make speaking feel effortless."
        practice_sentence_2 = "I express my thoughts step by step with clarity and quiet confidence."

    next_practice_payload = {
        "title": "Next Practice",
        "instruction": "Repeat these 2 sentences three times. First slowly at a calm, steady pace, then at your natural speaking speed:",
        "sentences": [practice_sentence_1, practice_sentence_2],
        "difficult_words_note": difficult_words_practice,
        "mode": mode if is_twister_mode else "reading",
        "reason": "Practicing short targeted sentences builds muscle memory for smooth, unhurried speech."
    }

    actionable_drills = [
        {
            "title": "Gentle Onset & Articulation Pacing Drill",
            "steps": "1. Inhale gently for 3 seconds into your belly. 2. Start the first consonant with a soft breath release. 3. Commit to finishing the entire phrase without stopping or restarting."
        },
        {
            "title": "The Slow-to-Fast Articulation Stepper",
            "steps": "1. Articulate the phrase at 50% slow speed with exaggerated mouth shape. 2. Repeat at 75% natural speed. 3. Say it at normal conversational speed with relaxed jaw."
        }
    ]

    paragraph_match_payload = {
        "match_percentage": paragraph_match_result["match_pct"] if paragraph_match_result else 100.0,
        "matched_words_count": paragraph_match_result["matched_count"] if paragraph_match_result else word_count,
        "total_expected_words": paragraph_match_result["total_expected"] if paragraph_match_result else word_count,
        "missing_words": paragraph_match_result["missing"] if paragraph_match_result else [],
        "extra_words": paragraph_match_result["extra"] if paragraph_match_result else [],
        "replaced_words": paragraph_match_result["replaced"] if paragraph_match_result else [],
        "repeated_words": paragraph_match_result["repeated"] if paragraph_match_result else [],
        "is_reading_mode": bool(paragraph_match_result and paragraph_match_result.get("is_reading_mode")),
        "is_twister_mode": is_twister_mode,
        "mode_label": "Tongue Twister" if is_twister_mode else "Reading Mode",
        "summary": paragraph_match_result["summary"] if paragraph_match_result else "Speech analyzed."
    }

    return {
        "metrics": {
            "speaking_time_seconds": round(audio_duration_seconds, 1),
            "speaking_time_display": speaking_time_display,
            "words_spoken": word_count,
            "words_spoken_display": words_spoken_display,
            "speaking_rate_wpm": wpm,
            "speaking_rate_display": speaking_rate_display,
            "pace_status": pace_status,
            "long_pauses": long_pauses_count,
            "long_pauses_display": long_pauses_display,
            "natural_pauses": natural_pauses_count,
            "repetitions": repetition_count,
            "repetitions_display": repetitions_display,
            "repetitions_list": all_repetitions,
            "filler_words": filler_count,
            "filler_words_display": filler_words_display,
            "fillers_list": detected_fillers,
            "practice_score": practice_score,
            "practice_score_display": practice_score_display,
            "paragraph_match_pct": paragraph_match_payload["match_percentage"],
            "missing_words_count": len(paragraph_match_payload["missing_words"]),
            "extra_words_count": len(paragraph_match_payload["extra_words"]),
            "replaced_words_count": len(paragraph_match_payload["replaced_words"]),
            "repeated_words_count": len(paragraph_match_payload["repeated_words"]),
            "wpm": wpm,
            "word_count": word_count,
            "duration_seconds": round(audio_duration_seconds, 1),
            "filler_count": filler_count,
            "pauses_count": long_pauses_count + natural_pauses_count,
            "long_pauses_count": long_pauses_count,
            "repetitions_count": repetition_count,
            "clarity_score": paragraph_match_payload["match_percentage"] if paragraph_match_payload["is_reading_mode"] else (90 if not trailing_off else 80),
            "sentence_completion_pct": paragraph_match_payload["match_percentage"] if paragraph_match_payload["is_reading_mode"] else 100.0,
            "consistency_score": max(15.0, round(100.0 - total_deductions, 1))
        },
        "practice_score": practice_score,
        "practice_score_display": practice_score_display,
        "practice_score_focus": practice_score_focus,
        "pattern_noticed": pattern_noticed,
        "paragraph_match": paragraph_match_payload,
        "your_speech_feedback": {
            "what_went_well": what_went_well,
            "what_needs_improvement": what_needs_improvement,
            "main_difficulty_location": main_difficulty_location,
            "speech_pattern_noticed": pattern_noticed,
            "what_to_practise_next": "Practise reading the tongue twister again, starting slowly to coordinate consonant transitions before building speed." if is_twister_mode else "Practise reading the paragraph again, keeping eyes on each word and maintaining smooth pacing."
        },
        "what_went_well": what_went_well,
        "needs_improvement": needs_improvement_cards,
        "difficult_words": difficult_words,
        "difficult_words_practice": difficult_words_practice,
        "actionable_drills": actionable_drills,
        "next_practice": next_practice_payload,
        "transcript": transcript,
        "ai_service_configured": bool(custom_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")),
        "disclaimer": "FLUENCY speech analysis provides educational acoustic and behavioral speaking feedback. It does not provide medical diagnoses for speech disorders."
    }
