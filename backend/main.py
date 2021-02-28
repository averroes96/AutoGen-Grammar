from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist,defaultdict
import os,re,time
from operator import itemgetter

not_start = [".", "(", ")", "-", ",", ":", "``", "--"]

def only_tags(sent) -> str: # Function to get only the tags from a tagged sentence
    tokens = sent.split()
    temp = ""
    for token in tokens:
        temp += token.split("/")[1] + " "

    return temp

# Function to get all the tags presented in a given corpus 
# The corpust must be tagged

def get_corpus_tags(path)->str:

    sentences = open(path)
    tags = ""

    for sentence in sentences:
        sentence = only_tags(sentence)
        tags += sentence + " "

    fd = FreqDist(tags.split())

    return list(fd)


# Function to extract the all possible ngrams from a list of sents
def extract_ngrams(sents)->list:

    mygrams = []
    for sentence in sents:
        for i in range(2, len(sentence) - 1):
            temp = tuple(ngrams(sentence.split(), i))
            if len(temp) > 0:
                for tmp in temp:
                    if tmp[0] not in not_start:
                        #print(tmp)
                        mygrams.append(tmp)
                        #print(tmp)
            
            # I want to go to school
            # I want 

    return mygrams

# get all the sentences of a file | path:str = path of the file
def get_sents(path)->str:

    file = open(path).read().strip().split("\n")
    sents = []

    for line in file:
        if line.strip() == "":
            pass
        line = only_tags(line.strip())
        sents.append(line)

    return sents

# Substitution, replace in a list of sentences the tag by the rule name (needs revision)
def substitute(sents, rule):

    rule_text = rule[1][0] + " " + rule[1][1]
    rule_text_regex = rule_text + r"\s"

    for i in range(0, len(sents)-1):
        if rule_text in sents[i]:
            sents[i] = sents[i].replace(rule_text, rule[0])

    return sents

# get the current tags
def get_current_tags(sents,all_tags):

    tags = ""
    for sent in sents:
        sent = sent.split()
        for tag in sent:
            if tag in all_tags:
                tags += tag + " "

    return list(FreqDist(tags.split()))

def check_terminals(current, all):

    for tag1 in current:
        for tag2 in all:
            if tag1 == tag2:
                return True

    return False

# Main Algorithm

def run(path):

    all_tags = get_corpus_tags(path) # get all the tags of the original corpus
    current_sents = get_sents(path)
    rules = defaultdict(str)
    has_terminals = True
    cpt = 1

    while has_terminals:

        extracted_grams = extract_ngrams(current_sents)
        fd = FreqDist(extracted_grams)
        rule = ["NT" + str(cpt), fd.max()]
        rules[rule[0]] = rule[1]
        current_sents = substitute(current_sents, rule)
        current_tags = get_current_tags(current_sents, all_tags)
        if not check_terminals(current_tags, all_tags):
            has_terminals = False

        print(f"{rule[0]} => {rule[1]}")
        print(f"num tags = {len(current_tags)}")
        cpt+=1
        print("=" * 96)

    return rules

run("brown\\ca01")

#extracted_grams = extract_ngrams(get_sents("brown\\ca01"))

#print(extracted_grams[0])

#print(len(extracted_grams))

#print(fd.freq(("at", "nn")))
#print(fd[("at", "nn")])
#print(fd.max())