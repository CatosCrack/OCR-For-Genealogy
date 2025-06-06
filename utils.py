import re
import unicodedata

# Iterate over blocks to gather starting and ending indexes
def get_indexes(doc):
    block_idx = []
    
    for page in doc.pages:
        for block in page.blocks:
            start = block.layout.text_anchor.text_segments[0].start_index
            end = block.layout.text_anchor.text_segments[0].end_index
            block_idx.append((start, end))

    return block_idx

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

# Find names in text and get bounding boxes
def get_bounding_box(name, original_text, token_map):
    print("### Searching bounding box...")
    # Ensure the name is a string
    name = str(name)
    
    # Get initial and last index of text
    pattern = r"\b" + "".join(char + r"[\n-]*" if char != " " else r"[\s]*" for char in name ) + r"\b"
    match = re.search(pattern, original_text, re.IGNORECASE)
    if match:
        idx = match.span()[0]
        end = match.span()[1]+1 # Add one because Document AI considers whitespaces
        print("#### Indexes: ", idx, end, "String: ", repr(original_text[idx:end]))
        # Get bounding box
        first_token = token_map[idx]

        # Check if both indexes are contained inside one token
        if first_token[0] == idx and first_token[1] >= end:
            coordinates = []
            for pair in first_token[3]:
                coordinates.append({
                    "x": pair.x,
                    "y": pair.y
                })
            return coordinates
        # If not, find the next token and return a dict with the left coordinates of the first token and the right coordinates of the last token
        else:
            for idx in token_map:
                if token_map[idx][1] >= end:
                    second_token = token_map[idx]
                    return [{
                        "x": first_token[3][0].x,
                        "y": first_token[3][0].y
                    }, {
                        "x": second_token[3][1].x,
                        "y": second_token[3][1].y
                    }, {
                        "x": second_token[3][2].x,
                        "y": second_token[3][2].y
                    }, {
                        "x": first_token[3][3].x,
                        "y": first_token[3][3].y
                    }]
    else:
        print("No matches")