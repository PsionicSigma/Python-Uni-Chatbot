import os
import numpy as np
import time
import json
import datetime
import random
import nltk
from nltk import ngrams
import normalization

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
    print ("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X),len(X[0]),1, len(klases)) )
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(klases))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)
        
    for j in iter(range(epochs+1)):
        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
                
        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) )
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error )
                break
                
        # in what direction is the target value?
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
        
        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
        
        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))        
        
        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update
        
        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': klases
              }
    synapse_file = "synapses.json"

    with open(synapse_file, 'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)
    print ("saved synapses to:", synapse_file)


data = open('ANN_train_1.json', encoding="utf8").read()
intents = json.loads(data)

n_gramm = 1
words = []
klases = []
uzklausaWithTag = []
removed_ignore = []
words_gram = []
new_pattern = ""

list_uzklausos = []

for intent in intents['intents']:
    for pattern in intent['uzklausos']:
        list_uzklausos.append(pattern)
        for word in pattern.split():
            normalized_word = normalization.lem(word.lower())
            if normalized_word not in normalization.ignore_words:
                new_pattern = new_pattern + ' ' + normalized_word

        uzklausaWithTag.append((new_pattern.strip(), intent['tag']))
        ngram = ngrams(new_pattern.strip().split(), n_gramm)

        for g in ngram:
            words_gram.append(g)

        new_pattern = ""

        if intent['tag'] not in klases:
            klases.append(intent['tag'])

# remove duplicates
words = list(set(words_gram))
klases = list(set(klases))

# create our training data
training = []
output = []

# create an empty array for our output
output_empty = [0] * len(klases)

# training set, bag of words for each sentence
for doc in uzklausaWithTag:
    bag = []
    pattern_words = doc[0].split()
    pattern_words = [normalization.lem(w) for w in pattern_words]
    pattern_words = [w.lower() for w in pattern_words if w not in normalization.ignore_words]
    pattern = ' '.join(pattern_words)
    for w in words:
        bag.append(1) if ' '.join(w) in pattern else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[klases.index(doc[1])] = 1
    output.append(output_row)

x = np.array(training)
y = np.array(output)

print(len(training), len(output))

start_time = time.time()

train(x, y, hidden_neurons=15, alpha=0.05, epochs=100000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print ("Processing time:", elapsed_time, "seconds")
