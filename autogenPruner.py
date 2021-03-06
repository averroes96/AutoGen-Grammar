import func
import re
temp = func.get_tagged_sents("brown_corpus")

# Function to check if a sentence contains a foreign phrase
def contains_foreign_phrase(sent):

    tags = sent.split()
    for i in range(0, len(tags)):
        if tags[i-1].startswith("fw") and tags[i].startswith("fw") and tags[i+1].startswith("fw"):
            return True
        
    return False

# Function to remove hyphenated cited tags from sentence's tags
def remove_cited_tags(sent):
    
    tags = sent.split()
    for i in range(0, len(tags)):
        if "-nc" in tags[i]:
            tags[i] = tags[i].replace("-nc", "")

def separate_tags(sent):
    tags = sent.split()
    for i in range(0, len(tags)):
        if tags[i] == "uh":
            print(sent)

def regularize_corpus(path):
    #the grammer of the title and the headline wil be separated in a diff file ad generated ceparately 
    #as for hl ... it comes only in a separated sentence so we just omet it 
    #for title we replace it with tl tag
    #for foreign sentence we dont generate its grammer we just replace it with the tag fw if its more then one word
    #for sentences between cotes they will be written in there own line 
    #each sentence ends with ./.
    
    #open the file in string and correct it then rewrit in in the same file 
    f = open(path)
    file_contenante = f.read()
    f.close()
    file_contenante = file_contenante.replace("ppss+ber-n ","ppss+ber ")
    file_contenante = file_contenante.replace("t'hi-im/in+ppo ","to/in him/ppo ")
    file_contenante = file_contenante.replace("you's/ppss+bez ","you/ppss are/ber ") #me and you are (we can't write you're)
    file_contenante = file_contenante.replace("\n","_")
    list_quotes=re.findall("``/``.+?''/''",file_contenante)
    file_contenante=re.sub("``/``.+?''/''","/quotes",file_contenante)
    #cot -> ``/`` G ''/'' 
    #G -> one of rule_base |one of rule_base G 
    for quote in list_quotes:
        quote=re.sub("``/``|''/''","",quote)
        file_contenante =file_contenante +"_"+quote
    file_contenante = file_contenante.replace("_","\n")
    ########## will stop here the pre processing --- hl tl fw deal with in generation of grammer ############
    f = open(path, "w")    
    f.write(file_contenante)