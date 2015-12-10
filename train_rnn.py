import numpy as np
import csv
import itertools
import nltk
import operator
import sys
import time
from datetime import datetime
from utils import *
import matplotlib.pyplot as plt
import theano.tensor as T
import theano as theano

from rnn3 import *

vocabulary_size = 2688
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"
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
            pred_name = sentence_start_token + ' ' + argument + ' '
            # print 'got a predicate'
        elif tag == 'PREP':
            prep_name = argument + ' '
        elif tag == 'DOBJ':
            dobj_name = argument + ' '
        elif tag == 'PREDSTOP':
            temp_sentence = pred_name + dobj_name + prep_name + other_args + sentence_end_token
            sentence_array.append(temp_sentence)
            other_args = ''
            pred_name = ''
            prep_name = ''
            temp_sentence = ''
            dobj_name = ''
        else:
            other_args += argument + ' '

print "Parsed %d sentences." % (len(sentence_array))

tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentence_array]

# for i in np.arange(20):
#     print sentence_array[i]

# Count the word frequencies
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
print "Found %d unique words tokens." % len(word_freq.items())

# Get the most common words and build index_to_word and word_to_index vectors
vocab = word_freq.most_common(vocabulary_size - 1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])


w1 = csv.writer(open("csv_data/word_to_index.csv", "w"))
for key, val in word_to_index.items():
    w1.writerow([key, val])

with open("csv_data/index_to_word.csv", "wb") as f:
    for word in index_to_word:
        f.write(word + "\n")
#     writer.writerows(index_to_word)

# w2 = csv.writer(open("csv_data/index_to_word.csv", "w"))
# for word in index_to_word:
#     w2.writerow(word)

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


print "Created train set"

np.random.seed(10)
model = rnn3(vocabulary_size)
start = time.time()
model.sgd_step(X_train[10], y_train[10], 0.005)
end = time.time()
print end - start

# Uncomment to train RNN
# model = rnn3(vocabulary_size)
# losses = train_with_sgd(model, X_train[:8000], y_train[:8000], nepoch=12, evaluate_loss_after=1)
# save_model_parameters_theano('./models/trained-model-theano.npz', model)

# Uncomment to load RNN
# model = rnn3(vocabulary_size, hidden_dim=50)
model = rnn3(vocabulary_size)
load_model_parameters_theano('./models/trained-model-theano.npz', model)


def generate_sentence(model):
    # We start the sentence with the start token
    new_sentence = [word_to_index[sentence_start_token]]
    # print new_sentence
    # print new_sentence[-1]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[sentence_end_token]:
        next_word_probs = model.forward_propagation(new_sentence)
        sampled_word = word_to_index[unknown_token]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[unknown_token]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
    # for x in new_sentence:
    #     print x
    #     print index_to_word[x]
    sentence_str = [index_to_word[x] for x in new_sentence[1:-1]]
    return sentence_str

num_sentences = 10
senten_min_length = 16

for i in range(num_sentences):
    sent = []
    # We want long sentences, not sentences with one or two words
    while len(sent) < senten_min_length:
        sent = generate_sentence(model)
    print " ".join(sent)
