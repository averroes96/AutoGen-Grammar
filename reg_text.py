from nltk import ngrams
from nltk.corpus import brown
from nltk import FreqDist,defaultdict
import os,re,time
from operator import itemgetter
from glob import glob

training_data = [file for file in glob(r'brown\[c][a-j][0-9][0-9]')] # all files that starts with c[a-j] | represents 74% of the entire corpus 
# testing_data = [file for file in glob(r'brown\[c][k-r][0-9][0-9]')] # all files that starts with c[k-r] | represents 26% of the entire corpus 

# Get all the sentences of a certain corpus | used for separated corpus like brown
def get_tag_sents(path)->str:

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
        all_sents += get_tag_sents(file)

    return all_sents

def corpus_aio(data):

    all_sents = get_all_sents(data)
    mega_corpus = open("mega_corpus", "w")
    for sentence in all_sents:
        mega_corpus.write(sentence + "\n")

def corpus_pruning(path):

    content = open(path).read()
    content = content.replace("ppss+ber-n ","ppss+ber ")
    # What is "t'hi-im" ??
    content = content.replace("t'hi-im/in+ppo ","to/in him/ppo ")
    # There's no point of replacing "you're" by "you are", both are grammatically speaking right
    # content = content.replace("you're/ppss+bez ","you/ppss are/ber ") # me and you are (we can't write you're)
    list_cout = re.findall("``/``.+?''/''",content)
    content = re.sub("``/``.+?''/''","/cot", content)
    #cot -> ``/`` G ''/'' 
    #G -> one of rule_base |one of rule_base G 
    for cout in list_cout:
        cout=re.sub("``/``|''/''","",cout)
        content =content +"\n"+cout
    ########## will stop here the pre processing --- hl tl fw deal with in generation of grammer ############
    f = open("mega_corpus","w")    
    f.write(content)

#it doesnt deal with " " that are in multipple lines 
def regularize_corpus(training_data):

    for filename in training_data:
        #the grammer of the title and the headline wil be separated in a diff file ad generated separately 
        #as for hl ... it comes only in a separated sentence so we just omit it 
        #for title we replace it with tl tag
        #for foreign sentence we dont generate its grammer we just replace it with the tag fw if its more then one word
        #for sentences between quotes they will be written in there own line 
        #each sentence ends with ./.
        
        #open the file in string and correct it then rewrit in in the same file 
        f = open(filename)
        file_content = f.read()
        f.close()
        file_content = file_content.replace("ppss+ber-n ","ppss+ber ")
        file_content = file_content.replace("t'hi-im/in+ppo ","to/in him/ppo ")
        file_content = file_content.replace("you's/ppss+bez ","you/ppss are/ber ") #me and you are (we can't write you're)
        list_cout=re.findall("``/``.+?''/''",file_contenante)
        file_contenante=re.sub("``/``.+?''/''","/cot",file_contenante)
        #cot -> ``/`` G ''/'' 
        #G -> one of rule_base |one of rule_base G 
        for cout in list_cout:
            cout=re.sub("``/``|''/''","",cout)
            file_contenante =file_contenante +"\n"+cout
        ########## will stop here the pre processing --- hl tl fw deal with in generation of grammer ############
        f = open(filename,"w")    
        f.write(file_contenante)

def only_tags(sent) -> str: # Function to get only the tags from a tagged sentence
    tokens = sent.split()
    temp = ""
    for token in tokens:
        temp += token.split("/")[1] + " "

    return temp

def get_sents(path)->str:
    sents=[]
    for filename in os.listdir(path):
        for line in open(path+"/"+filename).read().strip().split("\n"):
            line = only_tags(line)
            sents.append(line)
    return list(sents)

#sentences = get_sents("brown_c")

#didnt finish it and didnt test it yet
def compress_tags(sentences):
    new_sentences=[]
    new_s=""
    for s in sentences:
        new_s=""
        tag = s.split()
        for i in range(0,len(tag)):
            # it could be a sentence of fw or a contatinated on like d'art (of art) it cant be concatinated in english
            # so if its not a single tag no + in it then its a fw tt court 
            if("fw"in tag[i]):
                j=i
                while("fw"in tag[j+1]and j<len(tag)):
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
                while("tl"in tag[j+1]and j<len(tag)):
                    j=j+1
                if(j<len(tag)):
                    i=j
                    tag[i]="tl" #foreign sentence
                else:
                    i=j-1
                    tag[i]="tl" #foreign sentence
            #case of headline
            if("hl"in tag[i]):
                j=i
                while("hl"in tag[j+1]and j<len(tag)):
                    j=j+1
                if(j<len(tag)):
                    i=j
                    tag[i]="hl" #foreign sentence
                else:
                    i=j-1
                    tag[i]="hl" #foreign sentence
            # ther's one tag "ppss+ber-n" -n in it has no meaning so im gonna omet it 
            #You're/ppss+ber-n replace it with You're/ppss+ber
            #until that point thers no tag that contains + and - in the same time 
            # seperate suffixes {$,s,+___,*}
            #starting with * ... thers 2 wordt with + and * at the same time 'tain't = it aint = it is not (pps+bez+*)
                                                                            #whyn't = why didn't = why did not 
            #so we'll start with + ... found 2 wrong abreviation : t'hi-im/IN+PPO correction to/IN him/PPO
            #                                                      you's/PPSS+BEZ correction you/PPSS are/BER
            if("+" in tag[i]):
                tag[i] = tag[i].replace("+"," ") # the 2nd part of the tag cant be a start of rule so well check it in n_gram
            
            #case of np 
            new_s = new_s+tag[i]+" "
        new_sentences.append(new_s.strip())
    
    return new_sentences
#sentences=compress_tags(sentences)

#regularize_corpus("brown")

#corpus_aio(training_data)

#corpus_pruning("mega_corpus")