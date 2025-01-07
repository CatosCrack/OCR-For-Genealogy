## This script processes the raw CSV files to capialize all names and last names correctly

import csv
import os
import pandas as pd

# Get a list of files in the current directory
current_dir = f"{os.getcwd()}/raw/"
files = os.listdir(current_dir)

# Iterate through each file and extract the content
for filename in files:
    content = []
    if filename.endswith(".csv"):
        with open(current_dir + filename, "r", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                if not row:
                    continue
                text = row[0].split()
                for i in range(len(text)):
                    text[i]=text[i].capitalize()
                content.append([" ".join(text)])
        with open(f"{os.getcwd()}/processed/{filename[:-4]}_processed.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(content)

# Update directories
current_dir = f"{os.getcwd()}/processed/"

# Remove first names from last name documents
with open(f"{current_dir}first_names_processed.csv") as f_file, open(f"{current_dir}last_names_processed.csv") as l_file:
    content = []
    f_reader = list(csv.reader(f_file))
    l_reader = csv.reader(l_file)
    for l_row in l_reader:
        flag = True
        for f_row in f_reader:
            if l_row[0] == f_row[0]:
                flag = False
                break
        if flag:
            content.append(l_row)
            
with open(f"{current_dir}last_names_processed.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(content)


