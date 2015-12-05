import numpy as np
import csv
import itertools
import nltk

vocabulary_size = 8000
unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"

# Read the data and append SENTENCE_START and SENTENCE_END tokens
print "Reading CSV file..."
with open('csv_data/chunked.csv', 'rb') as f:
    reader = csv.reader(f, skipinitialspace=True)
    reader.next()
    # for x in reader:
    # 	print x[1]
    # 	print 'next sentence'
    # Split full comments into sentences
    sentences = itertools.chain(*[nltk.sent_tokenize(x[1].decode('utf-8').lower()) for x in reader])
    # Append SENTENCE_START and SENTENCE_END
    # sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
# print "Parsed %d sentences." % (len(sentences))

# for sent in sentences:
# 	print sent

class RNNNumpy:

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
	        o[t] = softmax(self.V.dot(s[t]))
	    return [o, s]

	RNNNumpy.forward_propagation = forward_propagation

	def predict(self, x):
	    # Perform forward propagation and return index of the highest score
	    o, s = self.forward_propagation(x)
	    return np.argmax(o, axis=1)

	RNNNumpy.predict = predict

np.random.seed(10)
model = RNNNumpy(vocabulary_size)
o, s = model.forward_propagation(X_train[10])
print o.shape
print o