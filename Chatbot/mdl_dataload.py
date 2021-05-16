#file for data load

#imports
import numpy as np
import json

#data vars
synapse_0 = []
synapse_1 = []
words = []
classes = []
intents = []

#load data
def load_data():
    synapse_file = 'data\synapses.json' 
    with open(synapse_file) as data_file: 
        synapse = json.load(data_file) 
        synapse_0 = np.asarray(synapse['synapse0']) 
        synapse_1 = np.asarray(synapse['synapse1'])
        words = np.asarray(synapse['words'])
        classes = np.asarray(synapse['classes'])

    intent_file = open('data\knowledgebase.json', encoding="utf8").read()
    intents = json.loads(intent_file)