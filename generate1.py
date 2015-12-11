# load model and index-word dicts and list, generate some text


import json
from utils import load_model_parameters_theano, save_model_parameters_theano
from rnn3 import *

vocabulary_size = 3000
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"
unknown_token = "UNKNOWN_TOKEN"

word_to_index = {}
with open("csv_data/word_to_index.txt") as infile:
    lines = infile.readlines()
    for line in lines:
        split_line = line.rsplit(',', 1)
        key = (split_line[0]).rstrip('\n')
        word_to_index[key] = int((split_line[1])[:-1])
        print key, int((split_line[1])[:-1])



index_to_word = []
with open("csv_data/index_to_word.txt", "r") as infile:
    index_to_word = infile.readlines()


# print "word to index ", type(word_to_index)
# print word_to_index["deli"]
# print "index to word ", type(index_to_word)
# print index_to_word[0:4]
# print index_to_word[0:20]

model = rnn3(vocabulary_size)
# losses = train_with_sgd(model, X_train, y_train, nepoch=50)
# save_model_parameters_theano('./data/trained-model-theano.npz', model)
load_model_parameters_theano('./models/trained-model-theano.npz', model)


def generate_sentence(model):
    # We start the sentence with the start token
    new_sentence = [word_to_index[sentence_start_token]]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[sentence_end_token]:
        next_word_probs = model.forward_propagation(new_sentence)
        sampled_word = word_to_index[unknown_token]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[unknown_token]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
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