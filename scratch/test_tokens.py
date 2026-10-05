import sys
import unicodedata
import re

sys.stdout.reconfigure(encoding='utf-8')

punct = '.,!?:;\"“”«»‹›()[]{}।॥…–—/\\|`~*#@$%^&+=¿¡。、・「」『』〜！？：；'
pattern = r'[^\s' + re.escape(punct) + r']+'
strip_chars = punct + '\'\"-_'

def clean_tokens(text):
    if not text:
        return []
    text = unicodedata.normalize('NFC', text)
    tokens = []
    for m in re.finditer(pattern, text, re.UNICODE):
        tok = m.group(0).strip(strip_chars)
        if tok:
            tokens.append(tok.lower())
    return tokens

print('FR:', clean_tokens("L'histoire des civilisations est d'une beauté"))
print('HI:', clean_tokens("जब हम जल्दबाज़ी में 'बोलते' हैं, तो रंग-बिरंगी तितलियाँ!"))
print('MR:', clean_tokens("पावसाच्या दिवसांत निसर्गाचे सौंदर्य अधिकच खुलून दिसते."))
print('EN:', clean_tokens("Don't worry, it's a high-quality test."))
print('JA:', clean_tokens("サニーは 元気な 金色の こいぬです。"))
