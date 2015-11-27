# parsing and tokenizing recipe text

import csv
import itertools
import operator
import numpy as np
import os
import sys
from utils import *

# print os.pardir

# recipe_path = os.path.join(os.pardir, "/AllRecipesData/BananaMuffins-fulltext/almond-banana-chocolate-muffins.txt")

# print recipe_path

mypath = os.path.dirname(os.path.abspath(__file__))

parent_path = os.path.join(mypath, "../AllRecipesData/chunked/")


f = []
for (dirpath, dirnames, filenames) in os.walk(parent_path):
    f.extend(dirnames)
    break

print len(f)

# with open("../AllRecipesData/BananaMuffins-fulltext/almond-banana-chocolate-muffins.txt", 'rb') as f:
# 	print f.read()
	# reader = csv.reader(f, skipinitialspace=True)
    # reader.next()
    # # Split full comments into sentences
    # sentences = itertools.chain(*[nltk.sent_tokenize(x[0].decode('utf-8').lower()) for x in reader])
    # # Append SENTENCE_START and SENTENCE_END
    # sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
# print "Parsed %d sentences." % (len(sentences))