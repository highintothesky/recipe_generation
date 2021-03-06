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



class rnn2:
    def __init__(self, word_dim, hidden_dim=100, bptt_truncate=4):
        # Assign instance variables
        self.word_dim = word_dim
        self.hidden_dim = hidden_dim
        self.bptt_truncate = bptt_truncate
        # Randomly initialize the network parameters
        self.U = np.random.uniform(-np.sqrt(1./word_dim), np.sqrt(1./word_dim), (hidden_dim, word_dim))
        self.V = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (word_dim, hidden_dim))
        self.W = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (hidden_dim, hidden_dim))

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
	        s[t] = np.tanh(self.U[:,x[t]] + self.W.dot(s[t-1]))
	        # print self.V.dot(s[t])
	        o[t] = softmax(self.V.dot(s[t]))
	    return [o, s]
	 
	rnn2.forward_propagation = forward_propagation

	def predict(self, x):
	    # Perform forward propagation and return index of the highest score
	    o, s = self.forward_propagation(x)
	    return np.argmax(o, axis=1)

	rnn2.predict = predict

	def bptt(self, x, y):
	    T_bptt = len(y)
	    # Perform forward propagation
	    o, s = self.forward_propagation(x)
	    # We accumulate the gradients in these variables
	    dLdU = np.zeros(self.U.shape)
	    dLdV = np.zeros(self.V.shape)
	    dLdW = np.zeros(self.W.shape)
	    delta_o = o
	    delta_o[np.arange(len(y)), y] -= 1.
	    # For each output backwards...
	    for t in np.arange(T_bptt)[::-1]:
	        dLdV += np.outer(delta_o[t], s[t].T)
	        # Initial delta calculation
	        delta_t = self.V.T.dot(delta_o[t]) * (1 - (s[t] ** 2))
	        # Backpropagation through time (for at most self.bptt_truncate steps)
	        for bptt_step in np.arange(max(0, t-self.bptt_truncate), t+1)[::-1]:
	            # print "Backpropagation step t=%d bptt step=%d " % (t, bptt_step)
	            dLdW += np.outer(delta_t, s[bptt_step-1])              
	            dLdU[:,x[bptt_step]] += delta_t
	            # Update delta for next step
	            delta_t = self.W.T.dot(delta_t) * (1 - s[bptt_step-1] ** 2)
	    return [dLdU, dLdV, dLdW]
	 
	rnn2.bptt = bptt

def calculate_total_loss(self, x, y):
    L = 0
    # For each sentence...
    for i in np.arange(len(y)):
        o, s = self.forward_propagation(x[i])
        # We only care about our prediction of the "correct" words
        correct_word_predictions = o[np.arange(len(y[i])), y[i]]
        # Add to the loss based on how off we were
        L += -1 * np.sum(np.log(correct_word_predictions))
    return L
 
def calculate_loss(self, x, y):
    # Divide the total loss by the number of training examples
    N = np.sum((len(y_i) for y_i in y))
    return self.calculate_total_loss(x,y)/N

def gradient_check(self, x, y, h=0.001, error_threshold=0.01):
    # Calculate the gradients using backpropagation. We want to checker if these are correct.
    bptt_gradients = model.bptt(x, y)
    # List of all parameters we want to check.
    model_parameters = ['U', 'V', 'W']
    # Gradient check for each parameter
    for pidx, pname in enumerate(model_parameters):
        # Get the actual parameter value from the mode, e.g. model.W
        parameter = operator.attrgetter(pname)(self)
        print "Performing gradient check for parameter %s with size %d." % (pname, np.prod(parameter.shape))
        # Iterate over each element of the parameter matrix, e.g. (0,0), (0,1), ...
        it = np.nditer(parameter, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            ix = it.multi_index
            # Save the original value so we can reset it later
            original_value = parameter[ix]
            # Estimate the gradient using (f(x+h) - f(x-h))/(2*h)
            parameter[ix] = original_value + h
            gradplus = model.calculate_total_loss([x],[y])
            parameter[ix] = original_value - h
            gradminus = model.calculate_total_loss([x],[y])
            estimated_gradient = (gradplus - gradminus)/(2*h)
            # Reset parameter to original value
            parameter[ix] = original_value
            # The gradient for this parameter calculated using backpropagation
            backprop_gradient = bptt_gradients[pidx][ix]
            # calculate The relative error: (|x - y|/(|x| + |y|))
            relative_error = np.abs(backprop_gradient - estimated_gradient)/(np.abs(backprop_gradient) + np.abs(estimated_gradient))
            # If the error is to large fail the gradient check
            if relative_error > error_threshold:
                print "Gradient Check ERROR: parameter=%s ix=%s" % (pname, ix)
                print "+h Loss: %f" % gradplus
                print "-h Loss: %f" % gradminus
                print "Estimated_gradient: %f" % estimated_gradient
                print "Backpropagation gradient: %f" % backprop_gradient
                print "Relative Error: %f" % relative_error
                return
            it.iternext()
        print "Gradient check for parameter %s passed." % (pname)
 
rnn2.gradient_check = gradient_check
 
# Performs one step of SGD.
def numpy_sdg_step(self, x, y, learning_rate):
    # Calculate the gradients
    dLdU, dLdV, dLdW = self.bptt(x, y)
    # Change parameters according to gradients and learning rate
    self.U -= learning_rate * dLdU
    self.V -= learning_rate * dLdV
    self.W -= learning_rate * dLdW
 
rnn2.sgd_step = numpy_sdg_step
# Outer SGD Loop
# - model: The RNN model instance
# - X_train: The training data set
# - y_train: The training data labels
# - learning_rate: Initial learning rate for SGD
# - nepoch: Number of times to iterate through the complete dataset
# - evaluate_loss_after: Evaluate the loss after this many epochs
def train_with_sgd(model, X_train, y_train, learning_rate=0.005, nepoch=100, evaluate_loss_after=5):
    # We keep track of the losses so we can plot them later
    losses = []
    num_examples_seen = 0
    for epoch in range(nepoch):
        # Optionally evaluate the loss
        if (epoch % evaluate_loss_after == 0):
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "%s: Loss after num_examples_seen=%d epoch=%d: %f" % (time, num_examples_seen, epoch, loss)
            # Adjust the learning rate if loss increases
            if (len(losses) > 1 and losses[-1][1] > losses[-2][1]):
                learning_rate = learning_rate * 0.5 
                print "Setting learning rate to %f" % learning_rate
            sys.stdout.flush()
        # For each training example...
        for i in range(len(y_train)):
            # One SGD step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1




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

# for i in np.arange(20):
#     print sentence_array[i]

# Count the word frequencies
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
print "Found %d unique words tokens." % len(word_freq.items())
 
# Get the most common words and build index_to_word and word_to_index vectors
vocab = word_freq.most_common(vocabulary_size-1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
 
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



print "created train set"


np.random.seed(10)
model = rnn2(vocabulary_size)
o, s = model.forward_propagation(X_train[10])
# print o.shape
# print o

predictions = model.predict(X_train[10])
# print predictions.shape
# print predictions

print "predicted some"


 
rnn2.calculate_total_loss = calculate_total_loss
rnn2.calculate_loss = calculate_loss

print "calculatedd loss"

# Limit to 1000 examples to save time
# print "Expected Loss for random predictions: %f" % np.log(vocabulary_size)
# print "Actual loss: %f" % model.calculate_loss(X_train[:1000], y_train[:1000])


# To avoid performing millions of expensive calculations we use a smaller vocabulary size for checking.
grad_check_vocab_size = 100
np.random.seed(10)
model = rnn2(grad_check_vocab_size, 10, bptt_truncate=1000)
model.gradient_check([0,1,2,3], [1,2,3,4])

print "All gradient checks done"

np.random.seed(10)
model = rnn2(vocabulary_size)

start = time.time()
model.sgd_step(X_train[10], y_train[10], 0.005)
end = time.time()
print end - start

np.random.seed(10)
# Train on a small subset of the data to see what happens
model = rnn2(vocabulary_size)
losses = train_with_sgd(model, X_train[:100], y_train[:100], nepoch=10, evaluate_loss_after=1)