#file for ANN nodule

#imports
import numpy as np

#allowed error threshold
ERROR_THRESHOLD = 0.2

#return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, sentence_words, show_details=False):
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

#calculate sigmoid
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

#deduce results
def think(sentence, words, sentence_words, syn0, syn1, show_details=False):
    x = bow(sentence.lower(), words, sentence_words, show_details)
    if show_details: print ("sentence:", sentence, "\n bow:", x)
    l0 = x
    l1 = sigmoid(np.dot(l0, syn0))
    l2 = sigmoid(np.dot(l1, syn1))
    return l2

#classify sentence
def classify(sentence, words, sentence_words, classes, syn0, syn1, show_details=False):
    results = think(sentence, words, sentence_words, syn0, syn1, show_details)
    drop = [[i,r] for i,r in enumerate(results) if r<ERROR_THRESHOLD] 
    if not drop:
        return None
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD] 
    results.sort(key=lambda x: x[1], reverse=True)
    return_results =[[classes[r[0]],r[1]] for r in results]
    return return_results
