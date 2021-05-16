import nltk
from nltk import ngrams
import numpy as np
import json
import normalization

def classify(sentence, show_details=False):
    results = think(sentence, show_details)
    drop = [[i,r] for i,r in enumerate(results) if r<ERROR_THRESHOLD] 
    if not drop:
        return None
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[klases[r[0]],r[1]] for r in results]
    return return_results

def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details: print ("sentence:", sentence, "\n bow:", x)
    l0 = x
    l1 = sigmoid(np.dot(l0, synapse_0))
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [normalization.lem(w.lower()) for w in sentence_words]
    sentence_words = [w.lower() for w in sentence_words if w not in normalization.ignore_words]
    return sentence_words

    # new_pattern = ""
    # words_gram = []

    # for word in sentence.split():
    #     normalized_word = normalization.lem(word.lower())
    #     if normalized_word not in normalization.ignore_words:
    #         new_pattern = new_pattern + ' ' + normalized_word

    #     ngram = ngrams(new_pattern.strip().split(), 1)

    #     for g in ngram:
    #         words_gram.append(g)

    #     new_pattern = ""
                
    # return words_gram

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

ERROR_THRESHOLD = 0.2
synapse_file = 'synapses.json' 
with open(synapse_file) as data_file: 
    synapse = json.load(data_file) 
    synapse_0 = np.asarray(synapse['synapse0']) 
    synapse_1 = np.asarray(synapse['synapse1'])
    words = np.asarray(synapse['words'])
    klases = np.asarray(synapse['classes'])

data = open('pattern_match_KB.json', encoding="utf8").read()
intents = json.loads(data)

correct = 0
count = 0
for intent in intents['intents']:
    for pattern in intent['uzklausos']:
        result = classify(pattern)
        if result:
            print(result[0][0], " ", intent['tag'])
            if(result[0][0] == intent['tag']):
                correct += 1
        else: 
            print("nomatch ", intent['tag'])
            if(intent['tag'] == 'nomatch'):
                correct += 1
        count += 1

print(100 * correct / count, "% correct answers")

i = 0
correct = 0 
