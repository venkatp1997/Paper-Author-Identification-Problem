import pickle as pi
import tfidf
import numpy as np

def matching_keywords_pa(paperID,authorID):
    aKw=pi.load(open("aKw.p","rb"))
    kWp=pi.load(open("kWp.p","rb"))
    return set(aKw[authorID]).intersection(set(kWp[str(paperID)]))

def matching_keywords_aj(journalID,authorID):
    aKw=pi.load(open("aKw.p","rb"))
    jKw=pi.load(open("jKw.p","rb"))
    return set(aKw[authorID]).intersection(set(jKw[journalID]))

def matching_papers(authorID1,authorID2):
    aP=pi.load(open("aP1.p","rb"))
    return len(set(aP[authorID1]).intersection(set(aP[authorID2])))

def get_journal(paperID):
    PJ=pi.load(open("PJ.p","rb"))
    return PJ[paperID]

def get_authors(paperID):
    A=pi.load(open("A.p","rb"))
    print ("Done")
    return (A[paperID])

def noKeywords_Author(authorID):
    aKw=pi.load(open("aKw.p","rb"))
    return len(aKw[authorID])

def noKeywords_Paper(paperID):
    kWp=pi.load(open("kWp.p","rb"))
    return len(kWp[str(paperID)])

def vec(paperID,authorID):
    T=tfidf.tfidf("keywrd.p")
    T.create()
    vector=np.empty(0)
    #Feature-1
    ret=matching_keywords_pa(paperID,authorID)
    temp=np.empty(0)
    for keyword in ret:
        if len(keyword)==0: continue
        temp=np.append(temp,T.calculate(authorID,keyword))
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=16): break
    for k in range(j,16):
        vector=np.append(vector,0)

    journalID=get_journal(paperID)
    #Feature-2
    ret=matching_keywords_aj(journalID,authorID)
    temp=np.empty(0)
    for keyword in ret:
        if len(keyword)==0: continue
        temp=np.append(temp,T.calculate(authorID,keyword))
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=8): break
    for k in range(j,8):
        vector=np.append(vector,0)
    #Feature-3
    ret=get_authors(paperID)
    temp=np.empty(0)
    for i in ret:
        if i==authorID: continue
        temp=np.append(temp,matching_papers(i,authorID))
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    print (temp)
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=4): break
    for k in range(j,4):
        vector=np.append(vector,0)
    #Feature 4
    vector=np.append(vector,noKeywords_Author(authorID))
    #Feature 5
    vector=np.append(vector,noKeywords_Paper(paperID))
    return vector

