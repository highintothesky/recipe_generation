import numpy as np
import csv
import itertools
import nltk
import operator
import sys
from datetime import datetime
from utils import *
import matplotlib.pyplot as plt
import theano.tensor as Th


class rnn2:
    def __init__(self, word_dim, hidden_dim=100, bptt_truncate=4):
        # Assign instance variables
        self.word_dim = word_dim
        self.hidden_dim = hidden_dim
        self.bptt_truncate = bptt_truncate
        # Randomly initialize the network parameters
        self.U = np.random.uniform(-np.sqrt(1. / word_dim), np.sqrt(1. / word_dim), (hidden_dim, word_dim))
        self.V = np.random.uniform(-np.sqrt(1. / hidden_dim), np.sqrt(1. / hidden_dim), (word_dim, hidden_dim))
        self.W = np.random.uniform(-np.sqrt(1. / hidden_dim), np.sqrt(1. / hidden_dim), (hidden_dim, hidden_dim))

    def forward_propagation(self, x):
        # The total number of time steps
        T = len(x)
        # During forward propagation we save all hidden states in s because need them later.
        # We add one additional element for the initial hidden, which we set to 0
        s = np.zeros((T + 1, self.hidden_dim))
        s[-1] = np.zeros(self.hidden_dim)
        # The outputs at each time step. Again, we save them for later.
        o = np.zeros((T, self.word_dim))
        # For each time step...
        for t in np.arange(T):
            # Note that we are indxing U by x[t]. This is the same as multiplying U with a one-hot vector.
            s[t] = np.tanh(self.U[:, x[t]] + self.W.dot(s[t - 1]))
            print self.V.dot(s[t])
            o[t] = softmax(self.V.dot(s[t]))
        return [o, s]

        rnn2.forward_propagation = forward_propagation

    def predict(self, x):
        # Perform forward propagation and return index of the highest score
        o, s = self.forward_propagation(x)
        return np.argmax(o, axis=1)

        rnn2.predict = predict

vocabulary_size = 3000
sentence_start_token = "SENTENCE_START "
sentence_end_token = " SENTENCE_END"
unknown_token = "UNKNOWN_TOKEN"

# Read the data and append SENTENCE_START and SENTENCE_END tokens
print "Reading CSV file..."
sentence = ''
sentence_array = []
other_args = ''
pred_name = ''
prep_name = ''
temp_sentence = ''
dobj_name = ''
with open('csv_data/chunked.csv', 'rb') as f:
    reader = csv.reader(f, skipinitialspace=True)
    reader.next()
    for x in reader:
        tag = x[0]
        argument = x[1]
        if tag == 'PRED':
            pred_name = sentence_start_token + argument + ' '
            # print 'got a predicate'
        elif tag == 'PREP':
            prep_name = argument + ' '
        elif tag == 'DOBJ':
            dobj_name = argument + ' '
        elif tag == 'PREDSTOP':
            temp_sentence = pred_name + dobj_name + prep_name + other_args + sentence_end_token
            sentence_array.append(temp_sentence)
            # print sentence
            other_args = ''
            pred_name = ''
            prep_name = ''
            temp_sentence = ''
            dobj_name = ''
        else:
            # print 'no pred!'
            other_args += argument + ' '
        # if tag == 'PRED':
        #     sentence += sentence_start_token + argument + ' '
        #     # print 'got a predicate'
        # elif tag == 'PREDSTOP':
        #     sentence += sentence_end_token
        #     sentence_array.append(sentence)
        #     # print sentence
        #     sentence = ''
        # else:
        #     # print 'no pred!'
        #     sentence += argument + ' '


print "Parsed %d sentences." % (len(sentence_array))

tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentence_array]

# Count the word frequencies
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
print "Found %d unique words tokens." % len(word_freq.items())

# Get the most common words and build index_to_word and word_to_index vectors
vocab = word_freq.most_common(vocabulary_size - 1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])

print "Using vocabulary size %d." % vocabulary_size
print "The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1])

# Replace all words not in our vocabulary with the unknown token
for i, sent in enumerate(tokenized_sentences):
    tokenized_sentences[i] = [w if w in word_to_index else unknown_token for w in sent]

print "\nExample sentence: '%s'" % sentence_array[0]
print "\nExample sentence after Pre-processing: '%s'" % tokenized_sentences[0]

# Create the training data
X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])

np.random.seed(10)
model = rnn2(vocabulary_size)
o, s = model.forward_propagation(X_train[10])
print o.shape
print o
