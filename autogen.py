import nltk
from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist
import os,re,time
from operator import itemgetter
import time
import func
from autogenPruner import regularize_corpus
from collections import OrderedDict
import autogenTagger

def extract_ngrams(sents)->list:
    mygrams = []
    for sentence in sents:
        if(sentence!="" and len(sentence.split(" "))>1):
            for i in range(2, len(sentence)):
                mygrams += ngrams(sentence.split(), i)
    return mygrams

def sort_len(sentences):
    len_s = []
    for s in sentences :
        if len(s)not in len_s : len_s.append(len(s)) 
    sorted_sentences=[]
    for i in len_s:
        for s in sentences:
            if(len(s)==i):
                sorted_sentences.append(s)
    return sorted_sentences

rule_base = []

#extraction de regles
def run (path):
    rules = {}
    current_sents = func.get_tagged_sents(path)
    current_sents = func.compress_tags(current_sents)
    print("there's " + str(len(current_sents))+" sentences")
    text=""
    for s in current_sents : 
        if(" "in s):
            text = text+s+"\n"
    cpt=0
    while True:
        current_sents = text.split("\n")
        grams = extract_ngrams(current_sents)#get the n_grams
        fd = FreqDist(grams)
        max_freq_gram = fd.max()#r has the most frequente gram
        #print(max_freq_gram)
        if(fd[max_freq_gram]==1):
            break
        r="" #the string of the gram to be replaced
        for g in max_freq_gram:
            r = r + g + " "
        #exp ("at","nn") => r="at nn "   
        r = r.strip()
        rules["NT"+str(cpt)] = r
        text = text.replace(r + " ","NT"+str(cpt)+" ")#replace the gram by her rule name
        text=text.replace(r+"\n","NT"+str(cpt)+"\n")
        cpt+=1
    #all the gram do repeat one time only 
    #till here its correct the rest is not working at all 
    sentences = text.split("\n")
    sentences = sort_len(sentences)
    for i in range(0,len(sentences)):
        r = sentences[i]
        b = False # the rule is not a sub_rule
        if(text.count(r+" ")+text.count(r+"\n")>1):b=True # it is a sub rule
        if(len(sentences[i].split())>1):
            rules["NT"+str(cpt)]=r
            text=text.replace(r+" ","NT"+str(cpt)+" ")#replace the gram by her rule name
            text=text.replace(r+"\n","NT"+str(cpt)+"\n")
            if(b==False):rule_base.append("NT"+str(cpt))
            cpt=cpt+1
            sentences = text.split("\n")
            sentences = sort_len(sentences)
        else:
            if(b==False):rule_base.append(r)
    return rules


# func.corpus_light(func.get_sents("brown_corpus", "\n|./\.|./:"), 100)
# start = time.time()
# regularize_corpus("corpus_light")
# rules = run("corpus_light")
# end = time.time()
# print("total extracted "+str(len(rules))+" rule")
# print("and " + str(len(rule_base))+" different grammar")
# print("getting the rules took " + str((end-start)/60)+" min")

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

#at this point ull have a dict named rules that containes the noun of the rule or sub_rule with its tag
# and a list names rule_base that contains the diff racine de grammer

def save_grammar(rule_base, rules):

    grammar_file = open("grammar.cfg", "w")
    grammar_file.write("S -> ")
    rbs = ""
    for rule in rule_base:
        rbs = f"{rbs} | {rule}"
    rbs = rbs.replace("|", "", 1)
    grammar_file.write(f"{rbs}\n")

    res = OrderedDict(reversed(list(rules.items())))

    for key,val in res.items():
        new_val = val.split()
        for i in range(0, len(new_val)):
            if "NT" not in new_val[i]:
                new_val[i] = '"' + new_val[i] + '"'
        print(new_val)
        temp = " ".join(new_val)
        grammar_file.write(f"{key} -> {temp}\n")

# save_grammar(rule_base, rules)

grammarfile = nltk.data.load('file:grammar.cfg')

sentence = "play players to win"
tagger = autogenTagger.load_tagger("tagger.pkl")
token = tagger.tag(sentence.split())

tags = [tag[1] for tag in token]

# sent = "vb nns to vb".split()
rd = nltk.RecursiveDescentParser(grammarfile)
for tree in rd.parse(tags):
    print(tree)