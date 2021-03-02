from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist,defaultdict
import os,re,time
from operator import itemgetter

def only_tags(sent) -> str: # Function to get only the tags from a tagged sentence
    tokens = sent.split()
    temp = ""
    for token in tokens:
        temp += token.split("/")[1] + " "

    return temp

def get_corpus_tags(path)->str:

    sentences = open(path)
    tags = ""

    for sentence in sentences:
        sentence = only_tags(sentence)
        tags += sentence + " "

    fd = FreqDist(tags.split())

    return list(fd)

# Function to extract the all possible ngrams from a list of sents
#if thers 2 similar sentences it will not extract the nçgrams for the 2nd centence 
def extract_ngrams(sents)->list:

    mygrams = []
    for sentence in sents:
        for i in range(2, len(sentence) - 1):
            mygrams += ngrams(sentence.split(), i)
            
            # I want to go to school
            # I want 

    return mygrams

# get all the sentences of a file | path:str = path of the file
##################################################################################################
def get_sents(path)->str:

    file = open(path).read().strip().split("\n")
    sents = []

    for line in file:
        if line != "":############# changes here ###########
            line = only_tags(line)
            sents.append(line)

    return sents

# Substitution, replace in a list of sentences the tag by the rule name (needs revision)
def substitute(sents, rule):

    rule_text = rule[1][0] + " " + rule[1][1]
    rule_text_regex = rule_text + r"\s"

    for i in range(0, len(sents)-1):
        if rule_text in sents[i]:

            if "$" or "*" in rule_text:
                print(rule_text)
                sents[i] = sents[i].replace(rule_text, rule[0])
            else:
                sents[i] = re.sub(rule_text_regex, rule[0] + " ", sents[i])

    return sents

# get the current tags
#its the same as only tags but with list of sentences instead of path 
def get_current_tags(sents):

    tags = ""
    for sent in sents:
        sent = sent.split()
        for tag in sent:
            tags += tag + " "

    return list(FreqDist(tags.split()))

#check if the tag belongs to the corpus tags 
def check_terminals(current, all):

    for tag1 in current:
        for tag2 in all:
            if tag1 == tag2:
                return True

    return False

rule_base = []
#replace the gram by its rule name
def rplc(sents,gram,rule_name):
    #the sentences are already only tags
    r="" #the string of the grame to replace
    for g in gram:
        r=r+g+" "
    #exp ("at","nn") => r="at nn "    
    snt=[]
    for s in sents:
        stri=s.replace(r,rule_name+" ")
        if(len(stri.split()) > 1): snt.append(stri)
        else : rule_base.append(stri.strip())    
    return snt

#extraction de regles
def mm (path):
    rules = {}
    current_sents = get_sents(path)
    cpt=0
    while (len(current_sents)!=0):
        grams = extract_ngrams(current_sents)#get the n_grams
        fd = FreqDist(grams)
        r = fd.max()#r has the most frequente gram
        rules["NT" + str(cpt)] = r
        current_sents = rplc(current_sents,r,"NT"+str(cpt))#replace the gram by her rule name
        cpt += 1
    return rules

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

rules = mm("brown/ca01")
#at this point ull have a dict named rules that containes the noun of the rule or sub_rule with its tag
# and a list names rule_base that contains the diff racine de grammer

print(rule_base)
grammar_file = open("grammar.cfg", "w")
for rule in rule_base:
    #print(rule)
    if rule.startswith("NT"):
        grammar_file.write(f"{rule} -> ")
        terminals = ""
        for terminal in rules[rule]:
            terminals = f"{terminals} {terminal}"
        grammar_file.write(f"{rreplace(terminals,'|', '', 1)}\n")