# parsing and tokenizing recipe text. right now it only prints all the chunked recipes.
# the AllRecipesData folder should be in the same location as the recipe_generation folder

import csv
import os


mypath = os.path.dirname(os.path.abspath(__file__))
chunked_path = os.path.join(mypath, "../AllRecipesData/chunked/")

dirlist = []
for (dirpath, dirnames, filenames) in os.walk(chunked_path):
    dirlist.extend(dirnames)
    break

recipe_paths = []
for dirname in dirlist:
    recipe_type_path = os.path.join(chunked_path, dirname)
    for (dirpath, dirnames, filenames) in os.walk(recipe_type_path):
        for name in filenames:
            new_path = os.path.join(recipe_type_path, name)
            recipe_paths.append(new_path)

csv_path = os.path.join(mypath, "csv_data/chunked.csv")
writer = csv.writer(open(csv_path, 'w')) #, delimeter = ',', quoting = csv.QUOTE_NONE)
for recipe in recipe_paths:
    with open(recipe) as f:
        for line in f:
            if line != '\n':
                tokens = line.strip().split(':')
                if not((tokens[0] == 'SENTID') | (tokens[0] == 'SENT') | (tokens[0] == 'PREDID')):
                    if tokens[0] == "DOBJ":
                        writer.writerow((tokens[0], tokens[1].rsplit(' ', 1)[1]))
                    else: writer.writerow([tokens[0], tokens[1].replace('\"', '').strip()])
    writer.writerow(['STOP', '0'])