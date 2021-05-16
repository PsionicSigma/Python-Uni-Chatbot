#file for dialog control module

#imports
import json
import numpy as np

#import mdl_dataload
#from mdl_dataload import synapse_0, synapse_1, words, classes, intents
import mdl_preproc
import mdl_ANN

#process user input and return chatbot answer
def process_input(input_string):
    #mdl_dataload.load_data()
    ###
    synapse_file = 'data\synapses.json' 
    with open(synapse_file) as data_file: 
        synapse = json.load(data_file) 
        synapse_0 = np.asarray(synapse['synapse0']) 
        synapse_1 = np.asarray(synapse['synapse1'])
        words = np.asarray(synapse['words'])
        classes = np.asarray(synapse['classes'])

    intent_file = open('data\knowledgebase.json', encoding="utf8").read()
    intents = json.loads(intent_file)
    ###

    sentence = mdl_preproc.preprocess_sentence(input_string)
    sentence_words = mdl_preproc.clean_up_sentence(sentence)
    results = mdl_ANN.classify(sentence, words, sentence_words, classes, synapse_0, synapse_1)
    if not results:
        return 1, 'Deja, nesupratau Jūsų užklausos, jei norite, galite kreiptis į https://pagalba.vgtu.lt/ arba prašyti aptarnaujančio personalo pagalbos'

    print(results[0][0])
    print('===========================================')

    correct = 0
    count = 0
    for intent in intents['intents']:
        #print(intent['tag'])
        if results[0][0] == intent['tag']:
            #print('u pass butter')
            return 0, intent['atsakymas'][0]
        
    
    return 'response_string'
