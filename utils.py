import re
import unicodedata

# Find the fist occurrence of a year in a string of text
def extract_year(original_text):
    match = re.search(r"\b[^\d]\d{4}[^\d]\b", original_text)
    idx = match.span()[0]
    end = match.span()[1]
    return original_text[idx:end].replace(" ", "")

# Get blocks of text for processing
def get_text(idx, text):
    start = idx[0]
    end = idx[1]

    return text[start:end]

# Process text to remove new line charachters
def formatting(text_block):
    document_text = []
    i = 0
    while i < len(text_block):
        if text_block[i] == "-" and text_block[i+1] == "\n":
            document_text.append("")
            i += 2
        elif text_block[i] == "\n" and text_block[i-1] != "":
            document_text.append(" ")
            i += 1
        else:
            document_text.append(text_block[i])
            i += 1

    return "".join(document_text)

def remove_accent(text):
    normalized = []
    for char in text:
        if char != "ñ" and char != "Ñ" and not char.isascii():
            normal = unicodedata.normalize("NFD", char)
            for char in normal:
                if unicodedata.category(char) != "Mn":
                    normalized.append(char)
        else:
            normalized.append(char)

    return "".join(normalized)