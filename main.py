import nltk
from nltk import ngrams
from nltk.corpus import brown

#sentence = 'this is a foo bar sentences and i want to ngramize it'

def to_POSTagged_corpus(corpus): # Function takes as a parameter an organized corpus and turn it into a tagged one string

    data_file = ""

    for sent in corpus:
        for token in sent:
            data_file += f"{token[0]}/{token[1]} "
        data_file += "\n"

    return data_file
