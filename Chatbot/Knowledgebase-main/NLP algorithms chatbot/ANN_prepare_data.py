import nltk
from nltk import ngrams
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import os
import json
import normalization
import random

def prepare_data(data_json):

    data = open(data_json, encoding="utf8").read()
    intents = json.loads(data)

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
            ngram = ngrams(new_pattern.strip().split(), 1)

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

    training_words = []
    output_words = []

    # create an empty array for our output
    output_empty = [0] * len(klases)

    patterns_bags = []

    # training set, bag of words for each sentence
    for doc in uzklausaWithTag:
        bag = []
        pattern_words = doc[0].split()
        pattern_words = [normalization.lem(w.lower()) for w in pattern_words]
        pattern_words = [w.lower() for w in pattern_words if w not in normalization.ignore_words]
        pattern = ' '.join(pattern_words)
        training_words.append(pattern)
        for w in words:
            bag.append(1) if ' '.join(w) in pattern else bag.append(0)

        training.append(bag)
        # output is a '0' for each tag and '1' for current tag
        output_row = list(output_empty)
        output_words.append(doc[1])
        output_row[klases.index(doc[1])] = 1
        output.append(output_row)
        patterns_bags.append((pattern, bag, doc[1], output_row))

    return training, output, patterns_bags, klases, words
