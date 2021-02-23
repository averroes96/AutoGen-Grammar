import nltk
from nltk import ngrams

sentence = 'this is a foo bar sentences and i want to ngramize it'

n = 6
mygrams = []

for i in range(2, len(sentence) - 1):
    mygrams += ngrams(sentence.split(), i)

for grams in mygrams:
  print(grams)