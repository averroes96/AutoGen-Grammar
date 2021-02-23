from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist
import os
from operator import itemgetter
#sentence = 'this is a foo bar sentences and i want to ngramize it'

def to_POSTagged_corpus(corpus): # Function takes as a parameter an organized corpus and turn it into a tagged one string

    data_file = ""

    for sent in corpus:
        for token in sent:
            data_file += f"{token[0]}/{token[1]} "
        data_file += "\n"

    return data_file

def only_tags(sent) -> str: # Function to get only the tags from a tagged sentence
    tokens = sent.split()
    temp = ""
    for token in tokens:
        temp += token.split("/")[1] + " "

    return temp

def extract_ngrams(path):

    sentences = open(path).read().split("\n")
    print(len(sentences))
    mygrams = []
    for sentence in sentences:
        sentence = only_tags(sentence)
        #print(sentence)
        for i in range(2, len(sentence) - 1):
            mygrams += ngrams(sentence.split(), i)

    return mygrams

#sentence = "	The/at Fulton/np-tl County/nn-tl Grand/jj-tl Jury/nn-tl said/vbd Friday/nr an/at investigation/nn of/in Atlanta's/np$ recent/jj primary/nn election/nn produced/vbd ``/`` no/at evidence/nn ''/'' that/cs any/dti irregularities/nns took/vbd place/nn ./."

extracted_grams = extract_ngrams(os.getcwd() + "\\brown\\ca01")
print(extracted_grams[1])

fd = FreqDist(extracted_grams) # Calculate the frequency distribution of each ngram

sorted_tag_counts = sorted(fd.items(), key=itemgetter(1), reverse=True)
print([[(token,freq) for (token, freq) in sorted_tag_counts[:20]]])