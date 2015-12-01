# parsing and tokenizing recipe text. right now it only prints all the chunked recipes.
# the AllRecipesData folder should be in the same location as the recipe_generation folder

import numpy as np
import os
import nltk


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

print type(dirnames)
print type(new_path)
print len(recipe_paths)
print recipe_paths[200]

# TODO: parse the actual recipes in the recipe_paths list using nltk


# with open("../AllRecipesData/BananaMuffins-fulltext/almond-banana-chocolate-muffins.txt", 'rb') as f:
# 	print f.read()
	# reader = csv.reader(f, skipinitialspace=True)
    # reader.next()
    # # Split full comments into sentences
    # sentences = itertools.chain(*[nltk.sent_tokenize(x[0].decode('utf-8').lower()) for x in reader])
    # # Append SENTENCE_START and SENTENCE_END
    # sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
# print "Parsed %d sentences." % (len(sentences))