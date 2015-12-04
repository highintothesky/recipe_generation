import csv
import itertools
import operator
import numpy as np
import nltk
import sys
import os
from datetime import datetime

import matplotlib.pyplot as plt

import parse

mypath = os.path.dirname(os.path.abspath(__file__))
chunked_path = os.path.join(mypath, "../AllRecipesData/chunked/")
csv_path = os.path.join(mypath, "csv_data/chunked.csv")


print "Reading CSV file..."
with open(csv_path, 'r') as csv_file:
	csv_data = [data for data in csv.reader(csv_file)]
chunk_data = np.asarray(csv_data)