## This script creates annotations to train the Spacy NER model to recognize first names and last names
## and use the custom tags LAST_NAME and FIRST_NAME. This will train a model that will then check 
## PER entities in the AnCora corpus and replace PER with the custom tags.

import csv
import os
import random
import spacy
from spacy.tokens import DocBin

current_dir = os.getcwd()

# Create a list with the rows of the csv files
with open(f"{current_dir}/processed/first_names_processed.csv", "r", newline="") as file:
    reader = csv.reader(file, delimiter=",")
    first_names = []
    for row in reader:
        if not row:
            continue
        first_names.append(row[0])


with open(f"{current_dir}/processed/last_names_processed.csv", "r", newline="") as file:
    reader = csv.reader(file, delimiter=",")
    last_names = []
    for row in reader:
        if not row:
            continue
        last_names.append(row[0])

# Create a function to create annotations
def create_annotation(i, i_next, j, j_next, number):
    # Create a sentence
    match number:
        case 1:
            sentence = f"{first_names[i] + " " + last_names[j]} y {first_names[i_next] + " " + last_names[j_next]} se casaron en la iglesia de San Juan"

            # Find the index of first character of the each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])
            char3 = sentence.find(first_names[i_next])
            char4 = sentence.find(last_names[j_next])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME"),
                                    (char3, char3+len(first_names[i_next]), "FIRST_NAME"),
                                    (char4, char4+len(last_names[j_next]), "LAST_NAME")]}
        case 2:
            sentence = f"{first_names[i]} y {first_names[i_next]} compraron una casa en la loma"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(first_names[i_next])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(first_names[i_next]), "FIRST_NAME")]}
        case 3:
            sentence = f"{first_names[i] + " " + last_names[j]} le vendió a {first_names[i_next] + " " + last_names[j_next]} un lote en el Municipio de Socorro"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])
            char3 = sentence.find(first_names[i_next])
            char4 = sentence.find(last_names[j_next])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME"),
                                    (char3, char3+len(first_names[i_next]), "FIRST_NAME"),
                                    (char4, char4+len(last_names[j_next]), "LAST_NAME")]}
        case 4:
            sentence = f"La casa de {first_names[i] + " " + last_names[j]} se encuentra al lado de la iglesia principal"

            #Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME")]}
        case 5:
            sentence = f"La finca de {first_names[i]} se encuentra en la vereda de San Antonio"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME")]}
        case 6:
            sentence = f"{first_names[i]} y {first_names[i_next] + " " + last_names[j_next]} vendieron un lote a Nirmal {last_names[j]}"
            
            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(first_names[i_next])
            char3 = sentence.find(last_names[j_next])
            char4 = sentence.find("Nirmal")
            char5 = sentence.find(last_names[j])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(first_names[i_next]), "FIRST_NAME"),
                                    (char3, char3+len(last_names[j_next]), "LAST_NAME"),
                                    (char4, char4+len("Nirmal"), "FIRST_NAME"),
                                    (char5, char5+len(last_names[j]), "LAST_NAME")]}
        case 7:
            sentence = f"{first_names[i]} y {first_names[i_next] + " " + last_names[j_next]} le compraron a "
            sentence2 = f"{first_names[i_next] + " " + last_names[j_next]} un lote"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(first_names[i_next])
            char3 = sentence.find(last_names[j_next])
            char4 = len(sentence)+sentence2.find(first_names[i_next])
            char5 = len(sentence)+sentence2.find(last_names[j_next])

            sentence = sentence + sentence2

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                  (char2, char2+len(first_names[i_next]), "FIRST_NAME"),
                                  (char3, char3+len(last_names[j_next]), "LAST_NAME"),
                                  (char4, char4+len(first_names[i_next]), "FIRST_NAME"),
                                  (char5, char5+len(last_names[j_next]), "LAST_NAME")]}

        case 8:
            sentence = f"{first_names[i] + " " + last_names[j]} y {first_names[i_next] + " " + last_names[j_next]} fueron bautizados en la iglesia de San Pedro"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])
            char3 = sentence.find(first_names[i_next])
            char4 = sentence.find(last_names[j_next])

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME"),
                                    (char3, char3+len(first_names[i_next]), "FIRST_NAME"),
                                    (char4, char4+len(last_names[j_next]), "LAST_NAME")]}
        case 9:
            sentence = f"El papá de {first_names[i] + " " + last_names[j]} se llama {first_names[i_next]} "
            sentence2 = f"{last_names[j]}"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])
            char3 = sentence.find(first_names[i_next])
            char4 = len(sentence)+sentence2.find(last_names[j])

            sentence = sentence + sentence2

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME"),
                                    (char3, char3+len(first_names[i_next]), "FIRST_NAME"),
                                    (char4, char4+len(last_names[j]), "LAST_NAME")]}
        case 10:
            sentence = f"{first_names[i] + " " + last_names[j]} y "
            sentence2 = f"{first_names[i_next] + " " + last_names[j]} son hermanos e hijos de "
            sentence3 = f"{first_names[i_next] + " " + last_names[j]} y "
            sentence4 = f"{first_names[i_next] + " " + last_names[j]}"

            # Find the index of first character of each entity
            char1 = sentence.find(first_names[i])
            char2 = sentence.find(last_names[j])
            char3 = len(sentence)+sentence2.find(first_names[i_next])
            char4 = len(sentence)+sentence2.find(last_names[j])

            sentence = sentence + sentence2

            char5 = len(sentence)+sentence3.find(first_names[i_next])
            char6 = len(sentence)+sentence3.find(last_names[j])

            sentence = sentence + sentence3

            char7 = len(sentence)+sentence4.find(first_names[i_next])
            char8 = len(sentence)+sentence4.find(last_names[j])

            sentence = sentence + sentence4

            # Create a dictionary with the entities
            entities = {"entities":[(char1, char1+len(first_names[i]), "FIRST_NAME"),
                                    (char2, char2+len(last_names[j]), "LAST_NAME"),
                                    (char3, char3+len(first_names[i_next]), "FIRST_NAME"),
                                    (char4, char4+len(last_names[j]), "LAST_NAME"),
                                    (char5, char5+len(first_names[i_next]), "FIRST_NAME"),
                                    (char6, char6+len(last_names[j]), "LAST_NAME"),
                                    (char7, char7+len(first_names[i_next]), "FIRST_NAME"),
                                    (char8, char8+len(last_names[j]), "LAST_NAME")]}
        case _:
            pass
    
    # Provide entity data
    return (sentence, entities)


# Generate random annotations
annotations = []

for _ in range(20000):
    i = random.randint(0, len(first_names)-1)
    i_next = random.randint(0, len(first_names)-1)
    j = random.randint(0, len(last_names)-1)
    j_next = random.randint(0, len(last_names)-1)
    number = random.randint(1,10)
    annotations.append(create_annotation(i, i_next, j, j_next, number))

# Load a blank Spanish model and a DocBin object
nlp = spacy.blank("es")
db = DocBin()

# Fill the DocBin with the annotations
for text, annotation in annotations:
    doc = nlp(text)
    #for token in doc:
        #print(f"- Token: {token.text}, start: {token.idx}, end: {token.idx+len(token.text)}")
    
    ents = []
    seen_spans = ["placeholder"]
    
    for start, end, label in annotation["entities"]:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            for item in seen_spans:
                if span.text in item:
                    continue
                else:
                    print(f"Entity added: {span}. Start: {span.start}, End: {span.end}")
                    ents.append(span)
                    seen_spans.append(span)
                    break
        else:
            print("Text: ", text)
            print(f"Skipping entity: {start} - {end} - {label}")
            print(f"Skipped text: {text[start:end]}")
    
    print("Entities: ", ents)

    try:
        doc.ents = ents
        db.add(doc)
        #for ent in doc.ents:
            #print(f"Entity: {ent.text} - {ent.label_}")
    except:
        pass

# Save the DocBin to disk
db.to_disk(f"{current_dir}/training_data/dev.spacy")