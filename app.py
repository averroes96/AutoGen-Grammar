rule_base = []
#replace the gram by her rule name
def rplc(sents,gram,rule_name):
    #the sentences are already only tags
    r="" #the string of the grame to replace
    for g in gram:
        r=r+g+" "
    #exp ("at","nn") => r="at nn "    
    snt=[]
    for s in sents:
        stri=s.replace(r,rule_name+" ")
        if(len(stri.split())>1): snt.append(stri)
        else : rule_base.append(stri)    
    return snt

#extraction de regles
def mm (path):
    rules = {}
    current_sents = get_sents(path)
    cpt=0
    while (len(current_sents)!=0):
        grams=extract_ngrams(current_sents)#get the n_grams
        fd = FreqDist(grams)
        r = fd.max()#r has the most frequente gram
        rules["NT"+str(cpt)]=r
        current_sents=rplc(current_sents,r,"NT"+str(cpt))#replace the gram by her rule name
        cpt+=1
    return rules
rules =mm("brown/ca01")

(r not in racine or r==rule)): #and (r not in rule_base or r==rule)):
                    b=True
                    #replace r with its tags
                    rl = rl+st(rules[r])
                else : rl = rl + r + " "
        rule_tag[rule]=rl
    if(b):return rec_tag(rule_tag,rules,racine)
    return rule_tag
tag_rules=rec_tag(dict_rule,rules,racine)
    
def test_gram (sentence,grammer):
    b=False
    for r in grammer:
        if(r.strip()==sentence.strip()):return True
        if(grammer[r].strip() in sentence.strip()):
            b=True
            sentence = sentence.replace(grammer[r].strip(),r)
    if(b==True):return test_gram (sentence,grammer)
    return False

s ="in ap nns , at nn vbd cs : ( cd ) "
print(test_gram(s,tag_rules))

    
