# parsing and tokenizing recipe text. this version also takes ingredients
# into account
# the AllRecipesData folder should be in the same location as the recipe_generation folder

import csv
import os


mypath = os.path.dirname(os.path.abspath(__file__))
chunked_recipe_path = os.path.join(mypath, "../AllRecipesData/chunked/")
ingredient_path = os.path.join(mypath, "../AllRecipesData/fulltext/")


dirlist = []
for (dirpath, dirnames, filenames) in os.walk(chunked_recipe_path):
    dirlist.extend(dirnames)
    break

ingr_dirlist = []
for (dirpath, dirnames, filenames) in os.walk(ingredient_path):
    ingr_dirlist.extend(dirnames)
    break

recipe_paths = []
ingredient_paths = []
for dirname in dirlist:
    ind = dirlist.index(dirname)
    recipe_type_path = os.path.join(chunked_recipe_path, dirname)
    ingredient_type_path = os.path.join(ingredient_path, ingr_dirlist[ind])
    for (dirpath, dirnames, filenames) in os.walk(recipe_type_path):
        for name in filenames:
            new_recipe_path = os.path.join(recipe_type_path, name)
            recipe_paths.append(new_recipe_path)
            new_ingredient_path = os.path.join(ingredient_type_path, name)
            ingredient_paths.append(new_ingredient_path)

#trimBrack trimms "-rbl-" and "-rrb" strings from chucked data
def trimBrack(tokens):
    lrbstr = "-lrb-"
    rrbstr = "-rrb-"
    #trim DOBJ
    if tokens[0] == "DOBJ":
        if tokens[1].find(lrbstr) != -1:
            tokens[1] = tokens[1][:tokens[1].find(lrbstr)]
        if tokens[1].find(rrbstr) != -1:
            tokens[1] = tokens[1].replace("-rrb-","")
    #trim PARG
    elif tokens[0] == "PARG":
        if tokens[1].find(lrbstr) != -1:
            tokens[1] = tokens[1][:tokens[1].find(lrbstr)]
        if tokens[1].find(rrbstr) != -1:
            tokens[1] = tokens[1][:tokens[1].find(rrbstr)-1]
    #trim OARG
    elif tokens[0] == "OARG":
        if tokens[1].find(lrbstr) != -1:
            tokens[1] = tokens[1][:tokens[1].find(lrbstr)]
    #return trimmed token
    return tokens[1]

csv_path = os.path.join(mypath, "csv_data/chunked.csv")
ingr_path = os.path.join(mypath, "csv_data/ingr.csv")

try:
    os.remove(csv_path)
    print "csv file deleted"
except OSError:
    print "No csv file found!"

writer = csv.writer(open(csv_path, 'w')) #, delimeter = ',', quoting = csv.QUOTE_NONE)
writer2 = csv.writer(open(ingr_path, 'w'))
for recipe in recipe_paths:
    ingredient_txt = ingredient_paths[recipe_paths.index(recipe)]
    with open(ingredient_txt) as f1:
        found_ingr_list = False
        for line in f1:
            tokens = line.strip().split()
            # print tokens
            # print type(tokens)
            if not tokens and found_ingr_list == False:
                pass
            elif tokens[0] == "Ingredients" and found_ingr_list == False:
                found_ingr_list = True
            elif found_ingr_list == False:
                pass
            elif found_ingr_list == True and tokens[0] == "Data":
                found_ingr_list = False
                pass
            else:
                writer2.writerow(tokens)

    with open(recipe) as f:
        for line in f:
            if line != '\n':
                tokens = line.strip().split(':')
                if not((tokens[0] == 'SENTID') | (tokens[0] == 'SENT') | (tokens[0] == 'PREDID')):
                    if tokens[0] == "PRED":
                        writer.writerow(['PREDSTOP', 'PREDSTOP'])
                        writer.writerow([tokens[0], tokens[1].replace('\"', '').strip()])
                    elif tokens[0] == "DOBJ":
                        tokens[1] = trimBrack(tokens)
                        writer.writerow((tokens[0], tokens[1].rsplit(' ', 1)[1]))
                    elif tokens[0] == "PARG":
                        tokens[1] = trimBrack(tokens)
                        writer.writerow([tokens[0], tokens[1].replace('\"', '').strip()])
                    elif tokens[0] == "OARG":
                        tokens[1] = trimBrack(tokens)
                    else: writer.writerow([tokens[0], tokens[1].replace('\"', '').strip()])
    writer.writerow(['STOP', 'STOP'])
