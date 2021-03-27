from nltk import FreqDist
from nltk import ngrams
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
    print(sents[-1])
    corpus.close()

    return sents

def get_text_sents(text, sep = "\n")-> str:

    return re.split(sep, text.strip())

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
def corpus_light(sents, start = 0, max = 2000):
    
    new_sents = []

    print(f"Sentences: {start} => {max + start}")
    for i in range(start, max + start):
        new_sents.append(sents[i])

    new_corpus = open("corpus_light", "w")
    for sent in new_sents:
        new_corpus.write(sent + "\n")

def compress_tags(sentences):
    new_sentences=[]
    new_s=""
    text =""
    for s in sentences : text = text + s + "\n"
        
    text = text.replace("dts", "dt").replace("dti", "dt").replace("dtx", "dt")
    text = text.replace("abn","ab").replace("abx", "ab").replace("abl", "ab")
    text = text.replace("-tl", "")
    text = text.replace("-hl", "")
    #text = text.replace("+", " ")

    # concat_tags = ['PPSS BER', 'PPSS BEM', 'PPS HVZ', 'PPSS MD', 'PPS BEZ', 'PPSS HVD', 'MD HV', 'DT BEZ',
    #                'EX BEZ', 'PPSS HV', 'PPS MD', 'NP BEZ', 'PN HVZ', 'WPS BEZ', 'RB BEZ', 'VB PPO', 'WDT BEZ',
    #                'VB IN', 'VBG TO', 'NN HVZ', 'VBN TO', 'NN BEZ', 'WDT HVZ', 'WRB BEZ', 'WPS MD', 'NN MD',
    #                'JJR CS', 'PPS HVD', 'VB RP', 'EX MD', 'EX HVD', 'WPS HVZ', 'PN MD', 'VB TO', 'DT MD',
    #                'HV TO', 'MD TO', 'MD PPSS', 'NR MD', 'NN IN', 'RP IN', 'PN BEZ', 'WPS HVD', 'WDT DOD',
    #                'WRB DO', 'WRB IN', 'NP HVZ', 'WRB DOD', 'WRB MD', 'EX HVZ', 'PPSS VB', 'WRB BER', 'NNS MD',
    #                'PPSS BEZ*', 'RBR CS', 'NP MD', 'TO VB', 'DO PPSS', 'VB AT', 'WRB DOZ',
    #                'DT BEZ', 'RB CS', 'WRB DOD*', 'WDT BER', 'PN HVD']
    
    # for c_t in concat_tags :
    #     tag_plus = c_t.lower().replace(" ","+")
    #     text = text.replace(" "+c_t.lower()+" "," "+tag_plus+" ")
    #     text = text.replace(" "+c_t.lower()+"\n"," "+tag_plus+"\n")
    #     text = text.replace("\n"+c_t.lower()+" ","\n"+tag_plus+" ")
    #     text = text.replace("\n"+c_t.lower()+"\n","\n"+tag_plus+"\n")
        
    sentences = text.split("\n")
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
            # case of juccessive np ex : A./np B./np junio/np => np np np ==> np
            if("np"== tag[i]):
                j=i
                while(j+1<len(tag)and"np"== tag[j+1]):
                    j=j+1
                if(i!=j):
                    if(j<len(tag)):
                        i=j
                        tag[i]="np" 
                    else:
                        i=j-1
                        tag[i]="np" 
                        
            new_s = new_s+tag[i]+" "
            i=i+1
        new_sentences.append(new_s.strip())
        
    return new_sentences

def prune(text):

    text = text.replace("dts", "dt").replace("dti", "dt").replace("dtx", "dt")
    text = text.replace("abn","ab").replace("abx", "ab").replace("abl", "ab")
    text = text.replace("-tl", "")
    text = text.replace("-hl", "")

    # concat_tags = ['PPSS BER', 'PPSS BEM', 'PPS HVZ', 'PPSS MD', 'PPS BEZ', 'PPSS HVD', 'MD HV', 'DT BEZ',
    #                'EX BEZ', 'PPSS HV', 'PPS MD', 'NP BEZ', 'PN HVZ', 'WPS BEZ', 'RB BEZ', 'VB PPO', 'WDT BEZ',
    #                'VB IN', 'VBG TO', 'NN HVZ', 'VBN TO', 'NN BEZ', 'WDT HVZ', 'WRB BEZ', 'WPS MD', 'NN MD',
    #                'JJR CS', 'PPS HVD', 'VB RP', 'EX MD', 'EX HVD', 'WPS HVZ', 'PN MD', 'VB TO', 'DT MD',
    #                'HV TO', 'MD TO', 'MD PPSS', 'NR MD', 'NN IN', 'RP IN', 'PN BEZ', 'WPS HVD', 'WDT DOD',
    #                'WRB DO', 'WRB IN', 'NP HVZ', 'WRB DOD', 'WRB MD', 'EX HVZ', 'PPSS VB', 'WRB BER', 'NNS MD',
    #                'PPSS BEZ*', 'RBR CS', 'NP MD', 'TO VB', 'DO PPSS', 'VB AT', 'WRB DOZ',
    #                'DT BEZ', 'RB CS', 'WRB DOD*', 'WDT BER', 'PN HVD']
    
    # for c_t in concat_tags :
    #     tag_plus = c_t.lower().replace(" ","+")
    #     text = text.replace(" "+c_t.lower()+" "," "+tag_plus+" ")
    #     text = text.replace(" "+c_t.lower()+"\n"," "+tag_plus+"\n")
    #     text = text.replace("\n"+c_t.lower()+" ","\n"+tag_plus+" ")
    #     text = text.replace("\n"+c_t.lower()+"\n","\n"+tag_plus+"\n")

    return text