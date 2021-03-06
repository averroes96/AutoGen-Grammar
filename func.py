from nltk import FreqDist
import re

def only_tags(sent) -> str: # Function to get only the tags from a tagged sentence
    tokens = sent.split()
    temp = ""
    for token in tokens:
        tag = token.split("/")
        temp += tag[len(tag)-1] + " "

    return temp

# Get all the tags of a given corpus
def get_corpus_tags(path)->str:

    sentences = open(path)
    tags = ""

    for sentence in sentences:
        sentence = only_tags(sentence)
        tags += sentence + " "

    fd = FreqDist(tags.split())

    return list(fd)

# get all the tagged sentences of a file | path:str = path of the file
##################################################################################################
def get_tagged_sents(path)->str:

    sents=[]
    
    for line in re.split("\n|./\.|./:",open(path).read().strip()):
        if(line!=""):
            line = only_tags(line)
            sents.append(line)
    return list(sents)

# Get all the sentences of a certain corpus | used for separated corpus like brown
def get_sents(path, sep = "\n")-> str:

    corpus = open(path, "r")
    sents = re.split(sep, open(path).read().strip())
    corpus.close()

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

# Function to generate a new corpus from a larger one with a smaller number of sentences
# Max is by default == 2000
def corpus_light(sents, max = 2000):
    
    new_sents = []
    for i in range(0, max):
        new_sents.append(sents[i])

    new_corpus = open("corpus_light", "w")
    for sent in new_sents:
        new_corpus.write(sent + "\n")

def compress_tags(sentences):
    new_sentences=[]
    new_s=""
    for s in sentences:
        new_s=""
        tag = s.split()
        i=0
        while(i<len(tag)):
            # it could be a sentence of fw or a contatinated on like d'art (of art) it cant be concatinated in english
            # so if its not a single tag no + in it then its a fw tt court 
            if("fw"in tag[i]):
                j=i
                while(j+1<len(tag) and "fw"in tag[j+1]):
                    j=j+1
                if(j==i and "+" not in tag[i]):
                    tag[i] = tag[i].replace("fw-","")
                elif(j<len(tag)):
                    i=j
                    tag[i]="fs" #foreign sentence
                else:
                    i=j-1
                    tag[i]="fs" #foreign sentence
            if("nc"in tag[i]):#many word tagged in nc are normal words 
                 tag[i] = tag[i].replace("-nc","")
            #case of title
            if("tl"in tag[i]):
                j=i
                while(j+1<len(tag)and"tl"in tag[j+1] ):
                    j=j+1
                if(j<len(tag)):
                    i=j
                    tag[i]="tl" #title
                else:
                    i=j-1
                    tag[i]="tl" #title
            #case of headline
            if("hl"in tag[i]):
                j=i
                while(j+1<len(tag)and"hl"in tag[j+1]):
                    j=j+1
                if(j<len(tag)):
                    i=j
                    tag[i]="hl" #headline
                else:
                    i=j-1
                    tag[i]="hl" #headline
            
            #until that point thers no tag that contains + and - in the same time 
            # seperate suffixes {$,s,+___,*}
            #starting with * ... thers 2 wordt with + and * at the same time 'tain't = it aint = it is not (pps+bez+*)
                                                                            #whyn't = why didn't = why did not 
            
            #if("+" in tag[i]):
                #"tag[i] = tag[i].replace("+"," ") # the 2nd part of the tag cant be a start of rule so well check it in n_gram
            
            #case of np 
            new_s = new_s+tag[i]+" "
            i=i+1
        new_sentences.append(new_s.strip())
        
    return new_sentences

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()