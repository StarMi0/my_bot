import nltk

nltk.download('punkt')


def split_text_into_sentences(text: str, max_length=1000):
    sentences = nltk.tokenize.sent_tokenize(text)
    text_parts = []
    current_part = ""
    for sentence in sentences:
        if len(current_part) + len(sentence) <= max_length:
            current_part += sentence
        else:
            text_parts.append(current_part)
            current_part = sentence
    if current_part:
        text_parts.append(current_part)
    return text_parts
