from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist,defaultdict
import os,re,time
from operator import itemgetter

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

def extract_ngrams(sents):

    mygrams = []
    for sentence in sents:
        for i in range(2, len(sentence) - 1):
            mygrams += ngrams(sentence.split(), i)
            

    return mygrams


def get_sents(path):

    file = open(path).read().strip().split("\n")
    sents = []

    for line in file:
        if line == "":
            pass
        line = only_tags(line)
        sents.append(line)

    return sents

def check(text):

    tmp = text
    if "$" in tmp:
        print("replacing dollar sign")
        re.sub(r"[$]", "", tmp)

    print(tmp)
    return tmp

def substitute(sents, rule):

    rule_text = rule[1][0] + " " + rule[1][1]
    rule_text_regex = rule_text + r"\s"
    #rule_text_regex = check(rule_text_regex)
    #print(rule_text)
    #print(rule_text)
    for i in range(0, len(sents)-1):
        #print(sent)
        if rule_text in sents[i]:
            #print(rule[0])
            #sent.replace(rule_text, rule[0])
            if "$" or "*" in rule_text:
                #print("Somethin in the way")
                #print(rule[0])
                #print(type(sents[i]))
                #x = str(sents[i])
                print(rule_text)
                sents[i] = sents[i].replace(rule_text, rule[0])
            else:
                #print(rule[0])
                #print(sents[i])
                sents[i] = re.sub(rule_text_regex, rule[0] + " ", sents[i])
            #print(sent)

    return sents

def get_current_tags(sents):

    tags = ""
    for sent in sents:
        sent = sent.split()
        for tag in sent:
            tags += tag + " "

    return list(FreqDist(tags.split()))

def check_terminals(current, all):

    for tag1 in current:
        for tag2 in all:
            if tag1 == tag2:
                return True

    return False

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
        current_tags = get_current_tags(current_sents)
        if not check_terminals(current_tags, all_tags):
            has_terminals = False
        
        #if "$" in rule[1][1]:
        #    for sent in current_sents:
        #        print(sent)
        #   has_terminals = False

        print(f"{rule[0]} => {rule[1]}")
        cpt+=1
        print("=" * 96)

    return rules

#sentence = "	The/at Fulton/np-tl County/nn-tl Grand/jj-tl Jury/nn-tl said/vbd Friday/nr an/at investigation/nn of/in Atlanta's/np$ recent/jj primary/nn election/nn produced/vbd ``/`` no/at evidence/nn ''/'' that/cs any/dti irregularities/nns took/vbd place/nn ./."

 # Calculate the frequency distribution of each ngram

#sorted_tag_counts = sorted(fd.items(), key=itemgetter(1), reverse=True)
#print([[(token,freq) for (token, freq) in sorted_tag_counts[:20]]])

#print(tags)

extracted_rules = run("brown\\ca01")

for key,val in extracted_rules.items():
    print(f"{key} => {val}")