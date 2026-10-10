with open('scratch/build_conversation_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace content = ''' with content = r'''
text = text.replace("content = '''", "content = r'''", 1)

with open('scratch/build_conversation_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated build_conversation_engine.py with raw string!")
