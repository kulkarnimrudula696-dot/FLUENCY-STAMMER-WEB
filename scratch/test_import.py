# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import reading_content_i18n
hindi_passages = reading_content_i18n.HINDI_READING_PASSAGES

import importlib.util
spec = importlib.util.spec_from_file_location("gen_mr", os.path.abspath("scratch/generate_all_reading_i18n.py"))
gen_mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_mr)
marathi_passages = gen_mr.marathi_passages

print(f"Loaded {len(hindi_passages)} Hindi and {len(marathi_passages)} Marathi passages.")
