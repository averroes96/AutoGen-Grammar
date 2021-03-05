from pickle import dump,load
from nltk.corpus import brown
from nltk import UnigramTagger, DefaultTagger, BigramTagger, RegexpTagger
from glob import glob

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

# Get all the sentences of a certain corpus | used for separated corpus like brown
def get_sents(path)->str:

    file = open(path)
    file_list = file.read().strip().split("\n")
    sents = []

    for line in file_list:
        if line.strip() != "":
            sents.append(line)

    file.close()

    return sents

# Get all the sentences of the entire corpus | used for separated corpus like brown
def get_all_sents(files):

    all_sents = []
    for file in files:
        all_sents += get_sents(file)

    return all_sents

# Get the tagged words of a given sentence
def tagged_words(sent) -> str:
    tokens = sent.split()
    temp = []
    for token in tokens:
        word, tag = token.rsplit("/",1)
        temp.append((word, tag))

    return temp

# Get the tagged sentences of a given sentences
def tagged_sents(sents) -> str:

    tagged_sents = []
    for sent in sents:
        tagged_sents.append(tagged_words(sent))

    return tagged_sents
 
# Train model on te given tagged sentence
def train(tagged_sents):

    default_tagger = DefaultTagger("nn") # Simple tagger
    unigram_default_tagger = UnigramTagger(tagged_sents, backoff=default_tagger) # Unigram tagger using default tagger as a backoff
    bigram_unigram_default_tagger = BigramTagger(tagged_sents,backoff=unigram_default_tagger)  # Bigram tagger using unigram regex tagger as a backoff

    return bigram_unigram_default_tagger

def save(tagger):
    
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