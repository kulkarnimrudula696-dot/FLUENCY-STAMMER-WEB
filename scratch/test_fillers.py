import re
import unicodedata

# Pure hesitation fillers (always disfluencies in any context)
PURE_FILLERS = {
    'english': ["um", "umm", "ummm", "uh", "uhh", "uhhh", "er", "err", "ah", "ahh", "hmm", "hmmm", "erm"],
    'hindi': ["उम", "अह", "हम्म", "आं", "एर", "um", "uh", "er", "hmm"],
    'marathi': ["उम", "अह", "हम्म", "आं", "एर", "um", "uh", "er", "hmm"],
    'spanish': ["eh", "em", "emm", "este", "pues", "a ver"],
    'french': ["euh", "bah", "ben", "genre"],
    'german': ["äh", "ähm", "halt", "quasi", "na ja"],
    'japanese': ["ええと", "あの", "その", "なんか", "まあ"],
    'chinese': ["那个", "就是", "嗯", "啊", "然后"]
}

# Multi-word phrase fillers (always discourse stalls)
MULTIWORD_FILLERS = {
    'english': ["you know", "i mean", "sort of", "kind of", "so yeah", "you see", "as in"],
    'hindi': ["मतलब की", "देखा जाए तो", "आपको पता है", "सच कहूं तो"],
    'marathi': ["सांगायचं म्हणजे", "कसं आहे", "बघा ना", "खरं तर"],
    'spanish': ["o sea", "en plan", "tu sabes"],
    'french': ["du coup", "tu sais", "en fait"],
    'german': ["weißt du", "sozusagen"]
}

def detect_filler_words(transcript, language="English"):
    """
    Context-aware filler word detection for FLUENCY.
    Correctly distinguishes between functional grammar words (e.g. 'I like this', 'did well', 'so happy')
    and speech disfluency filler stalls (e.g. 'I, um, like this', 'like, totally', 'Well, um...', 'matlab').
    """
    if not transcript:
        return [], 0

    norm_lang = (language or "English").strip().lower()
    text = unicodedata.normalize('NFC', transcript)
    lower_text = text.lower()
    
    detected_counts = {}

    def add_filler(word, count=1):
        if count <= 0:
            return
        detected_counts[word] = detected_counts.get(word, 0) + count

    # 1. Multi-word phrase fillers
    all_multiwords = []
    for lang_key, phrases in MULTIWORD_FILLERS.items():
        all_multiwords.extend(phrases)
    all_multiwords = sorted(list(set(all_multiwords)), key=len, reverse=True)

    working_text = lower_text
    for phrase in all_multiwords:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        matches = len(re.findall(pattern, working_text))
        if matches > 0:
            add_filler(phrase, matches)
            working_text = re.sub(pattern, ' ___ ', working_text)

    # 2. Pure hesitation sound fillers (Always fillers)
    all_pure = []
    for lang_key, p_list in PURE_FILLERS.items():
        all_pure.extend(p_list)
    all_pure = set(all_pure)

    tokens = re.findall(r'[^\s,;!?:\"\'\(\)\[\]{}।॥…–—/]+', working_text)
    for word in tokens:
        cleaned = word.strip('.,!?:;\"\'`~*#@')
        if cleaned in all_pure:
            add_filler(cleaned, 1)

    # 3. Contextual 'like'
    for match in re.finditer(r'\blike\b', lower_text):
        start, end = match.start(), match.end()
        before = lower_text[:start].rstrip()
        after = lower_text[end:].lstrip()
        
        has_comma_before = before.endswith(',') or before.endswith(';')
        has_comma_after = after.startswith(',') or after.startswith(';')
        
        prev_words = [w for w in re.findall(r'\b[\w\']+\b', before) if w not in all_pure]
        next_words = [w for w in re.findall(r'\b[\w\']+\b', after) if w not in all_pure]
        
        prev_w = prev_words[-1] if prev_words else ""
        next_w = next_words[0] if next_words else ""
        
        # If preceded by subject pronoun (I, you, we, they, he, she) AND followed by object (this, that, a, an, the, my, to, etc.) -> Verb
        if prev_w in ['i', 'we', 'they', 'you', 'he', 'she', 'would', 'do', 'did', 'does', 'really', 'also']:
            if next_w in ['this', 'that', 'these', 'those', 'a', 'an', 'the', 'my', 'your', 'his', 'her', 'our', 'their', 'to', 'it', 'coffee', 'pizza', 'travel', 'books', 'movies', 'music', 'art']:
                continue
            if not has_comma_before and not has_comma_after:
                continue

        # If comparative preposition: "looks like", "sounds like", "just like", "much like"
        if prev_w in ['looks', 'sound', 'sounds', 'feel', 'feels', 'just', 'much', 'something', 'anything', 'nothing', 'seem', 'seems', 'act', 'acts', 'smell', 'smells', 'taste', 'tastes']:
            continue

        # If "like a" / "like this" without commas
        if not has_comma_before and not has_comma_after and next_w in ['a', 'an', 'the', 'this', 'that', 'these', 'those']:
            continue
                
        # Otherwise, if surrounded by punctuation, isolated, or colloquial stall -> Filler
        if has_comma_before or has_comma_after:
            add_filler("like", 1)
        elif not prev_w and next_w in ['i', 'we', 'it', 'you', 'they', 'he', 'she', 'what', 'there']:
            add_filler("like", 1)
        elif prev_w in ['was', 'were', 'is'] and next_w in ['so', 'really', 'just', 'totally', 'fun', 'cool']:
            add_filler("like", 1)

    # 4. Contextual 'well'
    # 'well' is a filler ONLY at the beginning of an utterance as a stalling intro: e.g. "Well, I think...", "Well, um..."
    if re.search(r'^\s*well\s*[,;.]|^\s*well\s+(?:i|we|it|you|um|uh|actually|maybe)\b', lower_text):
        add_filler("well", 1)

    # 5. Contextual 'so'
    # 'so' is a filler ONLY at the start of an utterance stalling before hesitation/phrase: e.g. "So, um...", "So, I was thinking..."
    if re.search(r'^\s*so\s*[,;.]|^\s*so\s+(?:um|uh|er|like|basically|actually)\b', lower_text):
        add_filler("so", 1)

    # 6. Contextual 'actually' / 'basically' / 'literally' / 'honestly'
    for adv in ['actually', 'basically', 'literally', 'honestly']:
        matches = len(re.findall(r'[,;]\s*' + adv + r'\s*[,;]|\b' + adv + r'\s*[,;]?\s*(?:um|uh|er|like)\b|^\s*' + adv + r'\s*[,;.]|(?:^|\b(?:um|uh|so))\s*,?\s*' + adv + r'\b', lower_text))
        if matches > 0:
            add_filler(adv, min(matches, lower_text.split().count(adv)))

    # 7. Contextual Hindi/Marathi fillers (मतलब / म्हणजे)
    if 'मतलब' in text or 'matlab' in lower_text:
        m_matches = len(re.findall(r'(?:^|[,;\s])(?:मतलब|matlab)(?:[,;\s]|$)', lower_text))
        if m_matches > 0:
            add_filler("मतलब", m_matches)

    if 'म्हणजे' in text or 'mhanje' in lower_text:
        mh_matches = len(re.findall(r'(?:^|[,;\s])(?:म्हणजे|mhanje)(?:[,;\s]|$)', lower_text))
        if mh_matches > 0:
            add_filler("म्हणजे", mh_matches)

    # Format result
    detected = [{"word": w, "count": c, "type": "filler"} for w, c in detected_counts.items() if c > 0]
    total_count = sum(d["count"] for d in detected)
    return detected, total_count

test_cases = [
    ("I like this movie.", 0, "'like' as verb should NOT be a filler"),
    ("I, um, like this movie.", 1, "'um' detected as filler, 'like' is not"),
    ("It looks like rain today.", 0, "'looks like' should NOT be a filler"),
    ("Well, um, I actually like to travel.", 3, "'well', 'um', 'actually' detected"),
    ("She did very well on the exam.", 0, "'very well' should NOT be a filler"),
    ("He was so happy to see us.", 0, "'so happy' should NOT be a filler"),
    ("So, um, basically I was thinking about it.", 3, "'so', 'um', 'basically' detected as fillers"),
    ("You know, it was, like, really fun.", 2, "'you know' and 'like' detected as fillers"),
    ("Mujhe yeh pasand hai, matlab, mujhe accha laga", 1, "'matlab' detected as filler"),
    ("Mala coffee aavdate, mhanje, roz sakali", 1, "'mhanje' detected as filler")
]

all_passed = True
for idx, (sentence, expected_count, note) in enumerate(test_cases):
    det, cnt = detect_filler_words(sentence)
    status = "PASS" if cnt == expected_count else f"FAIL (got {cnt}, expected {expected_count})"
    if cnt != expected_count:
        all_passed = False
    print(f"Test {idx+1}: [{status}] - count: {cnt} (expected: {expected_count}) | Fillers: {det}")

print("\nOverall Status:", "ALL TESTS PASSED!" if all_passed else "SOME TESTS FAILED")
