
# coding: utf-8

# In[2]:

import pickle as pi
import tfidf
import vecfeature
import random


# In[2]:

#aP=pi.load(open("aP.p","rb"))
#aKw=pi.load(open("aKw.p","rb"))
#kWp=pi.load(open("kWp.p","rb"))
#jKw=pi.load(open("jKw.p","rb"))
#PJ=pi.load(open("PJ.p","rb"))
#A=pi.load(open("A.p","rb"))
#T=tfidf.tfidf("aKw.p")


# In[8]:

# Returns tuple of a list of features given authorID. (First Index: True)
def train_test(authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor):
    pos=[]
    neg=[]
    neg_sample_paperIDs=[]
    if authorID in aP:
        for i in aP[authorID]:
            pos.append(vecfeature.vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
    len_neg=2*(len(pos)+1)
    while True:
        neg_sample_keys=random.sample(list(aP),len_neg)
        neg_sample=[]
        flag=0
        for i in neg_sample_keys:
            if i==authorID:
                flag=1
        if flag==0:
            for i in neg_sample_keys:
                neg_sample.append(aP[i])
            break
    for i in neg_sample:
        for j in i:
            neg_sample_paperIDs.append(j)
    for i in neg_sample_paperIDs:
        neg.append(vecfeature.vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
    return (pos,neg)

