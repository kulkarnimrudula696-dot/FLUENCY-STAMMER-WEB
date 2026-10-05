# -*- coding: utf-8 -*-
"""
Assembles all language passages into reading_content_i18n.py
"""
import sys
import os
import pprint

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

# Import modules from scratch
import importlib.util

def load_module(mod_name, path):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

hindi_mod = load_module("hindi", "reading_content_i18n.py")
hindi_list = hindi_mod.HINDI_READING_PASSAGES

mr_mod = load_module("marathi", "scratch/generate_all_reading_i18n.py")
marathi_list = mr_mod.marathi_passages

es_mod = load_module("spanish", "scratch/build_western_languages.py")
spanish_list = es_mod.spanish_passages

fr_mod = load_module("french", "scratch/build_french.py")
french_list = fr_mod.french_passages

de_mod = load_module("german", "scratch/build_german.py")
german_list = de_mod.german_passages

ja_mod = load_module("japanese", "scratch/build_japanese.py")
japanese_list = ja_mod.japanese_passages

zh_mod = load_module("chinese", "scratch/build_chinese.py")
chinese_list = zh_mod.chinese_passages

print(f"Loaded:")
print(f"  Hindi: {len(hindi_list)}")
print(f"  Marathi: {len(marathi_list)}")
print(f"  Spanish: {len(spanish_list)}")
print(f"  French: {len(french_list)}")
print(f"  German: {len(german_list)}")
print(f"  Japanese: {len(japanese_list)}")
print(f"  Chinese: {len(chinese_list)}")

out_path = os.path.abspath("reading_content_i18n.py")
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""\n')
    f.write('FLUENCY Multi-Language Reading Content Library\n')
    f.write('Provides authentic, culturally natural, age-tailored reading passages across:\n')
    f.write('- Languages: English, Hindi, Marathi, Spanish, French, German, Japanese, Chinese\n')
    f.write('- 5 Age Groups: 6-11, 12-17, 18-23, 24-30, 31-40\n')
    f.write('- 3 Difficulties: easy, medium, hard\n')
    f.write('- 3 Lengths: short, medium, long\n')
    f.write('"""\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 1. HINDI (हिंदी)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('HINDI_READING_PASSAGES = ' + pprint.pformat(hindi_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 2. MARATHI (मराठी)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('MARATHI_READING_PASSAGES = ' + pprint.pformat(marathi_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 3. SPANISH (Español)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('SPANISH_READING_PASSAGES = ' + pprint.pformat(spanish_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 4. FRENCH (Français)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('FRENCH_READING_PASSAGES = ' + pprint.pformat(french_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 5. GERMAN (Deutsch)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('GERMAN_READING_PASSAGES = ' + pprint.pformat(german_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 6. JAPANESE (日本語)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('JAPANESE_READING_PASSAGES = ' + pprint.pformat(japanese_list, indent=4, width=120) + '\n\n')

    f.write('# -----------------------------------------------------------------------------\n')
    f.write('# 7. CHINESE (中文)\n')
    f.write('# -----------------------------------------------------------------------------\n')
    f.write('CHINESE_READING_PASSAGES = ' + pprint.pformat(chinese_list, indent=4, width=120) + '\n\n')

    f.write('''
# Mapping of all localized reading collections
READING_CONTENT_BY_LANG = {
    'hindi': HINDI_READING_PASSAGES,
    'hi': HINDI_READING_PASSAGES,
    'marathi': MARATHI_READING_PASSAGES,
    'mr': MARATHI_READING_PASSAGES,
    'spanish': SPANISH_READING_PASSAGES,
    'es': SPANISH_READING_PASSAGES,
    'french': FRENCH_READING_PASSAGES,
    'fr': FRENCH_READING_PASSAGES,
    'german': GERMAN_READING_PASSAGES,
    'de': GERMAN_READING_PASSAGES,
    'japanese': JAPANESE_READING_PASSAGES,
    'ja': JAPANESE_READING_PASSAGES,
    'chinese': CHINESE_READING_PASSAGES,
    'zh': CHINESE_READING_PASSAGES
}

VALID_AGE_GROUPS = ["6-11", "12-17", "18-23", "24-30", "31-40"]

def normalize_age_group(age_group):
    if not age_group:
        return "18-23"
    val = str(age_group).strip().replace("–", "-")
    if val in VALID_AGE_GROUPS:
        return val
    try:
        age = int(val)
        if age <= 11:
            return "6-11"
        elif age <= 17:
            return "12-17"
        elif age <= 23:
            return "18-23"
        elif age <= 30:
            return "24-30"
        else:
            return "31-40"
    except (TypeError, ValueError):
        pass
    legacy_map = {
        "6-9": "6-11", "10-12": "12-17", "13-17": "12-17",
        "18-25": "18-23", "26-32": "24-30", "33-40": "31-40"
    }
    return legacy_map.get(val, "18-23")


def get_localized_reading_passages(language="English", age_group="18-23", difficulty="all", length_type="all"):
    """
    Retrieve authentic, localized reading passages for the given language,
    age group, difficulty, and length.
    Ensures that non-English languages NEVER fall back to English content.
    """
    norm_lang = (language or "English").strip().lower()
    
    # If English or empty, return empty list so caller can query English READING_CONTENT
    if norm_lang in ["english", "en"]:
        return []

    collection = READING_CONTENT_BY_LANG.get(norm_lang)
    if not collection:
        # Check partial match (e.g. "español", "français", "deutsch")
        for key in READING_CONTENT_BY_LANG:
            if key in norm_lang or norm_lang in key:
                collection = READING_CONTENT_BY_LANG[key]
                break
    
    if not collection:
        # If language code was not found, default to Hindi or Spanish instead of English
        collection = HINDI_READING_PASSAGES

    norm_age = normalize_age_group(age_group)
    
    diff = (difficulty or "all").lower().strip()
    diff_map = {
        "easy": "easy", "beginner": "easy",
        "medium": "medium", "intermediate": "medium",
        "hard": "hard", "advanced": "hard"
    }
    if diff in diff_map:
        diff = diff_map[diff]
        
    len_type = (length_type or "all").lower().strip()

    # Filter by age group
    filtered = [p for p in collection if p.get("age_group") == norm_age]
    if not filtered:
        filtered = [p for p in collection if p.get("age_group") == "18-23"]

    # Filter by difficulty
    if diff != "all":
        diff_filtered = [p for p in filtered if p.get("difficulty") == diff]
        if diff_filtered:
            filtered = diff_filtered

    # Filter by length
    if len_type != "all":
        len_filtered = [p for p in filtered if p.get("length_type") == len_type]
        if len_filtered:
            filtered = len_filtered

    return filtered
''')

print("Successfully written reading_content_i18n.py!")
