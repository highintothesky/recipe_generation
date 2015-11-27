# parsing and tokenizing recipe text. right now it only prints all the chunked recipes.
# the AllRecipesData folder should be in the same location as the recipe_generation folder

import csv
import itertools
import operator
import numpy as np
import os
import sys
from utils import *


mypath = os.path.dirname(os.path.abspath(__file__))

chunked_path = os.path.join(mypath, "../AllRecipesData/chunked/")


dirlist = []
for (dirpath, dirnames, filenames) in os.walk(chunked_path):
    dirlist.extend(dirnames)
    break

for dirname in dirlist:
	recipe_type_path = os.path.join(chunked_path, dirname)
	print recipe_type_path
	for (dirpath, dirnames, filenames) in os.walk(recipe_type_path):
		print filenames
 #    	break

# with open("../AllRecipesData/BananaMuffins-fulltext/almond-banana-chocolate-muffins.txt", 'rb') as f:
# 	print f.read()
	# reader = csv.reader(f, skipinitialspace=True)
    # reader.next()
    # # Split full comments into sentences
    # sentences = itertools.chain(*[nltk.sent_tokenize(x[0].decode('utf-8').lower()) for x in reader])
    # # Append SENTENCE_START and SENTENCE_END
    # sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
# print "Parsed %d sentences." % (len(sentences))