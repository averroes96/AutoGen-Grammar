from pickle import dump,load
from nltk import UnigramTagger, DefaultTagger, BigramTagger

patterns = [
 (r".*ing$", "VBG"), # gerunds
 (r".*ed$", "VBD"), # simple past
 (r".*es$", "VBZ"), # 3rd singular present
 (r".*ould$", "MD"), # modals
 (r".*\"s$", "NN$"), # possessive nouns
 (r".*s$", "NNS"), # plural nouns
 (r"^-?[0-9]+(.[0-9]+)?$", "CD"), # cardinal numbers
 (r".*", "NN") # nouns (default)
 ]
 
# Train model on te given tagged sentence
def train(tagged_sents):

    default_tagger = DefaultTagger("nn") # Simple tagger
    unigram_default_tagger = UnigramTagger(tagged_sents, backoff=default_tagger) # Unigram tagger using default tagger as a backoff
    bigram_unigram_default_tagger = BigramTagger(tagged_sents,backoff=unigram_default_tagger)  # Bigram tagger using unigram regex tagger as a backoff

    return bigram_unigram_default_tagger

def save_tagger(tagger):
    
    output = open("tagger.pkl", "wb")
    dump(tagger, output, -1)
    output.close()

def load_tagger(path):

    input = open(path, "rb")
    tagger = load(input)
    input.close()

    return tagger

# Evaluate a model based on the given test dataset 
def evaluate(model, test):
    return model.evaluate(test)


##################################### You can use this as an example on how to train the model #################################################

# training_data = [file for file in glob(r'brown\[c][a-j][0-9][0-9]')] # all files that starts with c[a-j] | represents 74% of the entire corpus 
# testing_data = [file for file in glob(r'brown\[c][k-r][0-9][0-9]')] # all files that starts with c[k-r] | represents 26% of the entire corpus 

# training_tagged_sents = tagged_sents(get_all_sents(training_data))
# testing_tagged_sents = tagged_sents(get_all_sents(testing_data))

# tagger = train(training_tagged_sents)    

# print(evaluate(tagger, testing_tagged_sents))