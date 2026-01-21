import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def split_into_sentences(text):
    return [s.strip() for s in text.split('.') if s.strip()]
