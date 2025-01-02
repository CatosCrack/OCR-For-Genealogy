## This script creates annotations to train the Spacy NER model to recognize first names and last names
## and use the custom tags LAST_NAME and FIRST_NAME

import csv
import os
import random

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
            entities = {"entities":[
                (0,len(first_names[i])-1,"FIRST_NAME"),
                (len(first_names[i]),len(last_names[j])-1,"LAST_NAME"),
                (len(first_names[i_next])+2,len(first_names[i_next])-1, "FIRST_NAME"),
                (len(first_names[i_next]),len(last_names[j_next])-1, "LAST_NAME")
            ]}
        case 2:
            sentence = f"{first_names[i]} y {first_names[i_next]} compraron una casa en la loma"
            entities = {"entities":[
                (0, len(first_names[i])-1, "FIRST_NAME"),
                (len(first_names[i])+2, len(first_names[i_next])-1, "FIRST_NAME")
            ]}
        case 3:
            sentence = f"{first_names[i] + " " + last_names[j]} le vendió a {first_names[i_next] + " " + last_names[j_next]} un lote en el Municipio de Socorro"
            entities = {"entities":[
                (0, len(first_names[i])-1, "FIRST_NAME"),
                (len(first_names[i]), len(last_names[j])-1, "LAST_NAME"),
                (len(last_names[j])+12, len(first_names[i_next])-1, "FIRST_NAME"),
                ()
            ]}
        case 4:
            sentence = f"La casa de {first_names[i] + " " + last_names[j]} se encuentra al lado de la iglesia principal"
        case 5:
            sentence = f"La finca de {first_names[i]} se encuentra en la vereda de San Antonio"
        case 6:
            sentence = f"{first_names[i]} y {first_names[i_next] + " " + last_names[j_next]} vendieron un lote a {first_names[i_next] + " " + last_names[j_next]}"
        case 7:
            sentence = f"{first_names[i]} y {first_names[i_next] + " " + last_names[j_next]} le compraron a {first_names[i_next] + " " + last_names[j_next]} un lote"
        case 8:
            sentence = f"{first_names[i] + " " + last_names[j]} y {first_names[i_next] + " " + last_names[j_next]} fueron bautizados en la iglesia de San Pedro"
        case 9:
            sentence = f"El papá de {first_names[i] + " " + last_names[j]} se llama {first_names[i_next] + " " + last_names[j]}"
        case 10:
            sentence = f"{first_names[i] + " " + last_names[j]} y {first_names[i_next] + " " + last_names[j]} son hermanos e hijos de {first_names[i_next] + " " + last_names[j]} y {first_names[i] + " " + last_names[j_next]}"
        case _:
            pass
    
    # Provide entity data
    entities = 
    return {sentence, entities}


# Generate random annotations
annotations = []

for _ in range(500):
    i = random.randint(0, len(first_names))
    i_next = random.randint(0, len(first_names))
    j = random.randint(0, len(last_names))
    j_next = random.randint(0, len(last_names))
    number = random.randint(1,10)
    annotations.append(create_annotation(i, i_next, j, j_next, number))