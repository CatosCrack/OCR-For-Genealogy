## This script processes the raw CSV files to capialize all names and last names correctly

import csv
import os

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
                content.append(" ".join(text))
        with open(f"{os.getcwd()}/processed/{filename[:-4]}_processed.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in content:
                writer.writerow([row])
