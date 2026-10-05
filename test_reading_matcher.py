import re
import difflib

def clean_tokens(text):
    if not text:
        return []
    # Extract words preserving hyphens and apostrophes, normalized to lowercase
    return [w.lower() for w in re.findall(r"[\w'-]+", text, re.UNICODE) if w.strip()]

def compare_reading_paragraph(expected_text, spoken_text):
    expected_words = clean_tokens(expected_text)
    spoken_words = clean_tokens(spoken_text)

    if not expected_words:
        return {
            "match_pct": 100.0,
            "matched_count": 0,
            "total_expected": 0,
            "missing": [],
            "extra": [],
            "replaced": [],
            "repeated": []
        }
    
    if not spoken_words:
        return {
            "match_pct": 0.0,
            "matched_count": 0,
            "total_expected": len(expected_words),
            "missing": expected_words,
            "extra": [],
            "replaced": [],
            "repeated": []
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
            # In expected paragraph but missing from speech
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
    # 1. Single word immediate repetition (e.g. "today today", "went went")
    for idx in range(len(spoken_words) - 1):
        if spoken_words[idx] == spoken_words[idx + 1]:
            rep_str = f"{spoken_words[idx]} {spoken_words[idx]}"
            if rep_str not in repeated_items:
                repeated_items.append(rep_str)

    # 2. 2-word phrase repetitions (e.g. "to the to the")
    for idx in range(len(spoken_words) - 3):
        p1 = f"{spoken_words[idx]} {spoken_words[idx+1]}"
        p2 = f"{spoken_words[idx+2]} {spoken_words[idx+3]}"
        if p1 == p2:
            if p1 not in repeated_items:
                repeated_items.append(p1)

    n_exp = len(expected_words)
    n_match = len(matched_words)
    raw_accuracy = (n_match / n_exp) * 100.0

    # Penalty for extra unrelated words
    # If user adds extra words that are not in the text, it lowers precision
    extra_penalty = min(50.0, (len(extra_words) / max(n_exp, 1)) * 40.0)
    
    # Penalty for replaced words
    replace_penalty = min(30.0, (len(replaced_words) / max(n_exp, 1)) * 30.0)

    match_pct = max(0.0, min(100.0, round(raw_accuracy - (extra_penalty * 0.5) - (replace_penalty * 0.5), 1)))

    return {
        "match_pct": match_pct,
        "matched_count": n_match,
        "total_expected": n_exp,
        "missing": missing_words,
        "extra": extra_words,
        "replaced": replaced_words,
        "repeated": repeated_items
    }

if __name__ == "__main__":
    # Test 1: Extra words
    exp = "Today I went to the market."
    spk = "Today I went to the market. Haan baad mein dekh lenge."
    r1 = compare_reading_paragraph(exp, spk)
    print("Test 1 (Extra speech):", r1)
    assert "haan" in r1["extra"] and "lenge" in r1["extra"]

    # Test 2: Missing words
    exp2 = "Sunny is a happy golden puppy with soft ears."
    spk2 = "Sunny is a golden puppy with ears."
    r2 = compare_reading_paragraph(exp2, spk2)
    print("Test 2 (Missing words):", r2)
    assert "happy" in r2["missing"] and "soft" in r2["missing"]

    # Test 3: Replaced words
    exp3 = "Today I went to the market."
    spk3 = "Today I went to the shop."
    r3 = compare_reading_paragraph(exp3, spk3)
    print("Test 3 (Replaced words):", r3)
    assert any(item["expected"] == "market" and item["spoken"] == "shop" for item in r3["replaced"])

    # Test 4: Repeated words
    exp4 = "Today I went to the market."
    spk4 = "Today today I went went to the market."
    r4 = compare_reading_paragraph(exp4, spk4)
    print("Test 4 (Repeated words):", r4)
    assert any("today today" in r for r in r4["repeated"])

    print("All prototype tests passed successfully!")
