import re
import unicodedata

PUNCT_CHARS_STR = '.,!?:;\"“”«»‹›()[]{}।॥…–—/\\|`~*#@$%^&+=¿¡。、・「」『』〜！？：；'
PUNCT_PATTERN = r'[^\s' + re.escape(PUNCT_CHARS_STR) + r']+'
PUNCT_STRIP_CHARS = PUNCT_CHARS_STR + '\'\"-_'

def clean_tokens(text):
    if not text:
        return []
    text = unicodedata.normalize('NFC', text)
    tokens = []
    for match in re.finditer(PUNCT_PATTERN, text, re.UNICODE):
        tok = match.group(0).strip(PUNCT_STRIP_CHARS)
        if tok:
            tokens.append(tok.lower())
    return tokens

def detect_filler_words(transcript, prompt_text="", language="English"):
    transcript = (transcript or "").strip()
    if not transcript:
        return [], 0

    norm_lang = (language or "English").lower()
    lower_text = transcript.lower()

    # If the user was reading a displayed prompt paragraph, extract words that genuinely belong to the prompt
    prompt_words = set(clean_tokens(prompt_text)) if prompt_text else set()

    # 1. Multi-word phrases
    multi_phrases_map = {
        'english': ['you know', 'i mean', 'sort of', 'kind of', 'so yeah', 'you see', 'more or less', 'as if'],
        'hindi': ['मतलब की', 'यानी कि', 'तो मतलब', 'जैसे कि'],
        'marathi': ['सांगायचं म्हणजे', 'म्हणजे काय', 'तसं बघायला गेलं तर'],
        'spanish': ['o sea', 'es decir', 'por así decirlo'],
        'french': ['du coup', 'en fait', 'genre de'],
        'german': ['sozusagen', 'na ja', 'wie gesagt']
    }

    phrases_to_check = list(multi_phrases_map.get('english', []))
    for lang_key, phrases in multi_phrases_map.items():
        if lang_key in norm_lang or norm_lang in lang_key:
            for p in phrases:
                if p not in phrases_to_check:
                    phrases_to_check.append(p)

    detected = {}
    total_count = 0

    # Mask multi-word phrases to avoid double counting
    masked_text = lower_text
    for phrase in phrases_to_check:
        if prompt_text and phrase in prompt_text.lower():
            continue

        pattern = r'\b' + re.escape(phrase) + r'\b'
        matches = len(re.findall(pattern, masked_text))
        if matches > 0:
            detected[phrase] = {'word': phrase, 'count': matches, 'type': 'phrase'}
            total_count += matches
            masked_text = re.sub(pattern, ' ___phr___ ', masked_text)

    # 2. Pure single-word fillers (always hesitation markers when spoken)
    pure_fillers = {
        # English
        'um', 'uh', 'er', 'ah', 'hmm', 'mm', 'mmm', 'mhm', 'umm', 'uhh', 'hmmm', 'erm', 'em', 'uhm', 'uh-huh',
        # Hindi
        'मतलब', 'यानी', 'उम', 'अह', 'हम्म', 'एम', 'अं',
        # Marathi
        'म्हणजे', 'उम', 'अं', 'हम्म',
        # Spanish / French / German
        'eh', 'este', 'euh', 'bah', 'ben', 'äh', 'ähm', 'halt', 'quasi'
    }

    tokens = clean_tokens(masked_text)

    # Helper to find nearest non-pure-filler tokens before/after position i
    def get_context_tokens(pos):
        prev_tok = ''
        for p in range(pos - 1, -1, -1):
            if tokens[p] not in pure_fillers and tokens[p] != '___phr___':
                prev_tok = tokens[p]
                break
        next_tok = ''
        for n in range(pos + 1, len(tokens)):
            if tokens[n] not in pure_fillers and tokens[n] != '___phr___':
                next_tok = tokens[n]
                break
        return prev_tok, next_tok

    for i, tok in enumerate(tokens):
        if tok in pure_fillers:
            if tok in prompt_words:
                continue
            detected[tok] = detected.get(tok, {'word': tok, 'count': 0, 'type': 'word'})
            detected[tok]['count'] += 1
            total_count += 1

        elif tok == 'like':
            if 'like' in prompt_words:
                continue

            prev_meaningful, next_meaningful = get_context_tokens(i)
            prev_immediate = tokens[i - 1] if i > 0 else ''
            next_immediate = tokens[i + 1] if i + 1 < len(tokens) else ''

            is_verb_subject = prev_meaningful in {
                'i', 'we', 'they', 'you', 'he', 'she', 'who', 'would', 'to', 'might',
                'could', 'should', 'do', 'did', 'does', 'dont', "don't", 'didnt', "didn't",
                'people', 'kids', 'everyone', 'someone', 'anyone'
            }

            is_verb_object = next_meaningful in {
                'this', 'that', 'these', 'those', 'it', 'them', 'him', 'her', 'me', 'us',
                'to', 'a', 'an', 'the', 'my', 'your', 'his', 'our', 'their', 'reading',
                'books', 'movies', 'music', 'food', 'playing', 'swimming', 'going',
                'doing', 'eating', 'having', 'learning', 'speaking', 'some', 'any', 'order'
            }

            is_comparative = prev_meaningful in {
                'look', 'looks', 'looked', 'sound', 'sounds', 'sounded', 'feel', 'feels',
                'felt', 'seem', 'seems', 'seemed', 'taste', 'tastes', 'act', 'acts', 'smell', 'smells'
            } or (prev_meaningful in {'is', 'was', 'are', 'were', 'been', 'just', 'more', 'much', 'something', 'anything', 'nothing'} and next_meaningful in {'a', 'an', 'the', 'this', 'that', 'me', 'him', 'her', 'them', 'us', 'home', 'water', 'fire', 'magic', 'summer', 'winter', 'rain'})

            if is_verb_subject and is_verb_object:
                # Definite transitive verb usage: "I like this", "I, um, like reading", "would like to order"
                pass
            elif is_comparative:
                # Comparative preposition usage: "looks like rain", "felt like magic"
                pass
            elif is_verb_subject and next_meaningful and not bool(re.search(r',\s*like\s*,|,\s*like\b|\blike\s*,', lower_text)):
                # Subject + verb without hesitation commas
                pass
            else:
                is_comma_isolated = bool(re.search(r',\s*like\s*,|,\s*like\b|\blike\s*,', lower_text))
                is_repetition = (prev_immediate == 'like' or next_immediate == 'like')
                is_hedging = (prev_meaningful in {'was', 'is', 'were', 'am'} and next_meaningful in {'really', 'totally', 'about', 'kind', 'so', 'just', 'insane', 'crazy', 'nervous', 'surprised', 'excited', 'shocked'})
                is_standalone_start = (i == 0 and next_meaningful in {'i', 'we', 'you', 'it', 'there', 'they', 'he', 'she', 'what', 'how'})
                is_discourse_marker = (prev_meaningful in {'and', 'so', 'but'} and next_meaningful in {'we', 'i', 'you', 'they', 'he', 'she', 'it'})

                if is_comma_isolated or is_repetition or is_hedging or is_standalone_start or is_discourse_marker or not is_verb_subject:
                    detected['like'] = detected.get('like', {'word': 'like', 'count': 0, 'type': 'word'})
                    detected['like']['count'] += 1
                    total_count += 1

        elif tok == 'well':
            if 'well' in prompt_words:
                continue

            prev_meaningful, next_meaningful = get_context_tokens(i)
            prev_immediate = tokens[i - 1] if i > 0 else ''
            
            is_adverb = prev_meaningful in {
                'very', 'as', 'doing', 'did', 'done', 'feel', 'feels', 'felt', 'went',
                'all', 'so', 'how', 'quite', 'fairly', 'pretty', 'speaks', 'spoke'
            } or next_meaningful in {
                'done', 'known', 'made', 'being', 'organized', 'suited', 'prepared',
                'received', 'spoken', 'written', 'established'
            }

            if not is_adverb:
                is_initial = (i == 0)
                is_comma_isolated = bool(re.search(r',\s*well\b|\bwell\s*,', lower_text))
                is_adjacent_filler = (prev_immediate in pure_fillers) or (tokens[i + 1] in pure_fillers if i + 1 < len(tokens) else False)
                if is_initial or is_comma_isolated or is_adjacent_filler:
                    detected['well'] = detected.get('well', {'word': 'well', 'count': 0, 'type': 'word'})
                    detected['well']['count'] += 1
                    total_count += 1

        elif tok == 'so':
            if 'so' in prompt_words:
                continue

            prev_meaningful, next_meaningful = get_context_tokens(i)
            is_adverb_so = next_meaningful in {
                'much', 'many', 'good', 'happy', 'far', 'fast', 'great', 'nice', 'bad',
                'cool', 'big', 'small', 'long', 'short', 'tired', 'busy', 'that', 'well',
                'clearly', 'smoothly', 'hard', 'easy'
            } or prev_meaningful in {'and', 'or', 'but', 'if', 'why'}

            if not is_adverb_so:
                is_initial = (i == 0)
                is_comma_isolated = bool(re.search(r',\s*so\b|\bso\s*,', lower_text))
                is_adjacent_filler = (tokens[i - 1] in pure_fillers if i > 0 else False) or (tokens[i + 1] in pure_fillers if i + 1 < len(tokens) else False)
                if (is_initial and is_adjacent_filler) or is_comma_isolated:
                    detected['so'] = detected.get('so', {'word': 'so', 'count': 0, 'type': 'word'})
                    detected['so']['count'] += 1
                    total_count += 1

        elif tok in {'actually', 'basically', 'literally', 'honestly'}:
            if tok in prompt_words:
                continue

            prev_meaningful, next_meaningful = get_context_tokens(i)
            prev_immediate = tokens[i - 1] if i > 0 else ''
            next_immediate = tokens[i + 1] if i + 1 < len(tokens) else ''

            is_adverb_modifier = (prev_meaningful in {'was', 'is', 'are', 'were', 'am', 'feels', 'felt', 'seems', 'seemed'} and next_meaningful in {'nervous', 'good', 'happy', 'tired', 'fine', 'true', 'happened', 'working', 'trying', 'here', 'there', 'different', 'difficult', 'easy', 'possible'})
            
            if not is_adverb_modifier:
                is_initial = (i == 0)
                is_comma_isolated = bool(re.search(r',\s*' + re.escape(tok) + r'\b|\b' + re.escape(tok) + r'\s*,', lower_text))
                is_adjacent_filler = (prev_immediate in pure_fillers) or (next_immediate in pure_fillers)
                if is_initial or is_comma_isolated or is_adjacent_filler:
                    detected[tok] = detected.get(tok, {'word': tok, 'count': 0, 'type': 'word'})
                    detected[tok]['count'] += 1
                    total_count += 1

    return list(detected.values()), total_count

test_cases = [
    ('A', 'I like this movie.', 0, '', 'English'),
    ('B', 'I, um, like this movie.', 1, '', 'English'),
    ('C', 'Uh, I think I should try again.', 1, '', 'English'),
    ('D', 'I um um think I can do it.', 2, '', 'English'),
    ('E', 'I, hmm, I was actually nervous.', 1, '', 'English'),
    ('F', 'I mm mm think that is fine.', 2, '', 'English'),
    ('G', 'Er, I am not sure.', 1, '', 'English'),
    ('H', 'Um, well, basically I arrived late, you know.', 4, '', 'English'),
    ('I (Prompt protection)', 'I like reading books.', 0, 'I like reading books.', 'English'),
    ('J (Grammatical like orders)', 'I would like to order a fresh garden salad.', 0, '', 'English'),
    ('K (Grammatical looks like)', 'It looks like rain outside today.', 0, '', 'English'),
    ('L (Filler like with commas)', 'I was, like, really surprised when they arrived.', 1, '', 'English'),
    ('M (Hindi Fillers)', 'मैं मतलब घर जा रहा था और उम थक गया था।', 2, '', 'Hindi'),
    ('N (Marathi Fillers)', 'मला म्हणजे खूप छान वाटले आणि सांगायचं म्हणजे अभ्यास पूर्ण झाला.', 2, '', 'Marathi')
]

print("--- NEW TEST RESULTS ---")
all_passed = True
for tc in test_cases:
    name = tc[0]
    text = tc[1]
    exp_count = tc[2]
    prompt = tc[3]
    lang = tc[4]
    fillers, count = detect_filler_words(text, prompt_text=prompt, language=lang)
    status = "PASS" if count == exp_count else "FAIL"
    if count != exp_count:
        all_passed = False
    print(f"Test {name}: count={count} (Expected: {exp_count}) -> [{status}]")

print(f"\nALL PASSED: {all_passed}")
