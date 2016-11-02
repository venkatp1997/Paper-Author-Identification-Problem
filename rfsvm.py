
# coding: utf-8

# In[1]:

import pickle as pi
import tfidf
import vecfeature
import random
import traintest
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from operator import itemgetter
import unsupervised
import pandas as pd
import levenshtein
import math
import numpy as np


# In[2]:

def random_forest(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T,args1,args2,aff_Author,aff_PaperAuthor):
    (pos,neg)=train_test(authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor)
    pos_out=[1]*len(pos)
    neg_out=[-1]*len(neg)
    pos+=neg
    for i in pos:
        for j in i:
            if math.isnan(j) or j==float('Inf'):
                j=500
    pos_out+=neg_out
    clfRF=RandomForestClassifier()
    clfRF.fit(pos,pos_out)
    test=[]
    predicted_pos=[]
    predicted_neg=[]
    for i in paperIDs:
        test.append(vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
    clfO=clfRF.predict(test)
    for i in range(len(clfO)):
        if clfO[i]==1:
            predicted_pos.append(paperIDs[i])
        else:
            predicted_neg.append(paperIDs[i])
    ans=[]
    ans_pos_sort=[]
    for i in range(len(predicted_pos)):
        ans_pos_sort.append((predicted_pos[i],unsupervised.score_of_lists(args1,args2[predicted_pos[i]])))
    ans_pos_sort=sorted(ans_pos_sort,key=itemgetter(1))
    ans_pos_sort[:]=ans_pos_sort[::-1]

    ans_neg_sort=[]
    for i in range(len(predicted_neg)):
        ans_neg_sort.append((predicted_neg[i],unsupervised.score_of_lists(args1,args2[predicted_neg[i]])))
    ans_neg_sort=sorted(ans_neg_sort,key=itemgetter(1))
    ans_neg_sort[:]=ans_neg_sort[::-1]

    for i in ans_pos_sort:
        ans.append(i[0])
    for i in ans_neg_sort:
        ans.append(i[0])
    return ans
def svm(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T,args1,args2):
    (pos,neg)=traintest.train_test(authorID,aKw,kWp,aP,jKw,PJ,A,T)
    pos_out=[1]*len(pos)
    neg_out=[-1]*len(neg)
    if(len(pos)!=0):
        pos+=neg
        pos_out+=neg_out
        clfRF=SVC()
        clfRF.fit(pos,pos_out)
        test=[]
        predicted_pos=[]
        predicted_neg=[]
        for i in paperIDs:
            test.append(vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
            clfO=clfRF.predict(test)
        for i in range(len(clfO)):
            if clfO[i]==1:
                predicted_pos.append(paperIDs[i])
            else:
                predicted_neg.append(paperIDs[i])
    else:
        predicted_pos=[]
        predicted_neg=[]
        for i in paperIDs:
            predicted_neg.append(i)
    ans=[]
    ans_pos_sort=[]
    for i in range(len(predicted_pos)):
        ans_pos_sort.append((predicted_pos[i],unsupervised.score_of_lists(args1,args2[predicted_pos[i]])))
    ans_pos_sort=sorted(ans_pos_sort,key=itemgetter(1))
    ans_pos_sort[:]=ans_pos_sort[::-1]

    ans_neg_sort=[]
    for i in range(len(predicted_neg)):
        ans_neg_sort.append((predicted_neg[i],unsupervised.score_of_lists(args1,args2[predicted_neg[i]])))
    ans_neg_sort=sorted(ans_neg_sort,key=itemgetter(1))
    ans_neg_sort[:]=ans_neg_sort[::-1]

    for i in ans_pos_sort:
        ans.append(i[0])
    for i in ans_neg_sort:
        ans.append(i[0])
    return ans


# In[10]:

random_forest(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T)


# In[3]:

aKw=pi.load(open("aKw.p","rb"))
print ("aKw")
kWp=pi.load(open("kWp.p","rb"))
print ("kWp")
aP=pi.load(open("aP1.p","rb"))
print ("aP")
jKw=pi.load(open("jKw.p","rb"))
print ("jKw")
PJ=pi.load(open("PJ.p","rb"))
print ("PJ")
A=pi.load(open("A.p","rb"))
print ("A")
T=tfidf.tfidf("aKw.p")
args=[]
for i in aP:
    args.append(i)
T.create(args)
print ("TF-IDF Done")
aff_Author=pi.load(open("aff_Author.p","rb"))
print ("aff_Author")
aff_PaperAuthor=pi.load(open("aff_PaperAuthor.p","rb"))
print ("aff_PaperAuthor")


# In[9]:

data=pd.read_csv("/home/venkat/Downloads/Test.csv")
input1=[]
for (index,i) in data.iterrows():
    in1=i["PaperIds"].split()
    in1=[int(i) for i in in1]
    in2=int(i["AuthorId"])
    input1.append((in1,in2))
f=open("output1.csv","w")
f.write("AuthorId,PaperIds")
f.write("\n")
f1=open("output2.csv","w")
f1.write("AuthorId,PaperIds")
f1.write("\n")
no=0
for i in input1:
    args1=[]
    args2={}
    authorID=i[1]
    paperIDs=i[0]
    if authorID in aKw:
        for j in aKw[authorID]:
            args1.append((j,T.calculate(authorID,j)))
#     print ("Args-1 Done")
    for j in paperIDs:
        args2[j]=[]
        if str(j) in kWp:
            for k in kWp[str(j)]:
                args2[j].append((k,T.calculate(authorID,k)))
#     print ("Args-2 Done")
    ret=random_forest(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T,args1,args2,aff_Author,aff_PaperAuthor)
    ret1=svm(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T,args1,args2)
    f.write(str(authorID))
    f.write(",")
    for j in ret:
        f.write(str(j))
        f.write(" ")
    f.write("\n")
    f1.write(str(authorID))
    f1.write(",")
    for j in ret1:
        f1.write(str(j))
        f1.write(" ")
    f1.write("\n")
    no+=1
    print (no)
f.close()
f1.close()


# In[6]:

def train_test(authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor):
    pos=[]
    neg=[]
    neg_sample_paperIDs=[]
    if authorID in aP:
        for i in aP[authorID]:
            pos.append(vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
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
        neg.append(vec(i,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor))
    return (pos,neg)


# In[8]:

def vec(paperID,authorID,aKw,kWp,aP,jKw,PJ,A,T,aff_Author,aff_PaperAuthor,nb_flag=0):
    vector=np.empty(0)
    #Feature-1
    ret=vecfeature.matching_keywords_pa(aKw,kWp,paperID,authorID)
    # print (ret)
    # print ("Ret Done")
    temp=np.zeros(50000)
    cnt=0
    for keyword in ret:
        if len(keyword)==0: continue
        temp[cnt]=T.calculate(authorID,keyword)
        cnt+=1
        # if(cnt%1000)==0: print ("Feature-1 Going on..")
    temp=np.resize(temp,cnt)
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=5): break
    for k in range(j,5):
        vector=np.append(vector,0)
    if(nb_flag==1):
        #Feature-1_neg
        ret=vecfeature.matching_keywords_pa_neg(aKw,kWp,paperID,authorID)
        temp=np.zeros(50000)
        cnt=0
        for keyword in ret:
            if len(keyword)==0: continue
            temp[cnt]=T.calculate(authorID,keyword)
            cnt+=1
        temp=np.resize(temp,cnt)
        temp=np.sort(temp,axis=None)
        temp[:]=temp[::-1]
        j=0
        for i in temp:
            vector=np.append(vector,i)
            j+=1
            if(j>=5): break
        for k in range(j,5):
            vector=np.append(vector,0)

    journalID=vecfeature.get_journal(PJ,paperID)
    # print ("Feature-1 Done")
    #Feature-2
    ret=vecfeature.matching_keywords_aj(aKw,jKw,journalID,authorID)
    # print (ret)
    temp=np.zeros(50000)
    cnt=0
    for keyword in ret:
        if len(keyword)==0: continue
        temp[cnt]=T.calculate(authorID,keyword)
        cnt+=1
    temp=np.resize(temp,cnt)
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=3): break
    for k in range(j,3):
        vector=np.append(vector,0)
    # print ("Feature-2 Done")
    if(nb_flag==1):
        #Feature-2_neg
        ret=vecfeature.matching_keywords_aj_neg(aKw,jKw,journalID,authorID)
        temp=np.zeros(50000)
        cnt=0
        for keyword in ret:
            if len(keyword)==0: continue
            temp[cnt]=T.calculate(authorID,keyword)
            cnt+=1
        temp=np.resize(temp,cnt)
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
    ret=vecfeature.get_authors(A,paperID)
    temp=np.zeros(50000)
    cnt=0
    for i in ret:
        if i==authorID: continue
        temp[cnt]=vecfeature.matching_papers(aP,i,authorID)
        # if(cnt%1000)==0: print ("Feature-3 Going on..")
        cnt+=1
    temp=np.resize(temp,cnt)
    temp=np.sort(temp,axis=None)
    temp[:]=temp[::-1]
    j=0
    for i in temp:
        vector=np.append(vector,i)
        j+=1
        if(j>=4): break
    for k in range(j,4):
        vector=np.append(vector,0)
    if(nb_flag==1):
        #Feature-3_neg
        ret=vecfeature.get_authors(A,paperID)
        temp=np.zeros(50000)
        cnt=0
        for i in ret:
            if i==authorID: continue
            temp[cnt]=vecfeature.matching_papers_neg(aP,i,authorID)
            cnt+=1
        temp=np.resize(temp,cnt)
        temp=np.sort(temp,axis=None)
        temp[:]=temp[::-1]
        j=0
        for i in temp:
            vector=np.append(vector,i)
            j+=1
            if(j>=4): break
        for k in range(j,4):
            vector=np.append(vector,0)
    # print ("Feature-3 Done")
    #Feature 4
    vector=np.append(vector,vecfeature.noKeywords_Author(aKw,authorID))
    # print ("Feature-4 Done")
    #Feature 5
    vector=np.append(vector,vecfeature.noKeywords_Paper(kWp,paperID))
    # print ("Feature-5 Done")
    word1=""
    word2=""
    max2=0
    max3=0
    min4=500
    min5=500
    if authorID in aff_Author:
        word1=aff_Author[authorID]
    if authorID in aff_PaperAuthor:
        word2=aff_PaperAuthor[authorID]
    vector=np.append(vector,levenshtein.distance(word1,word2))
    if paperID in A:
        for i in A[paperID]:
            word3=""
            word4=""
            if i not in aff_Author and len(word1)==0:
                max2=max(max2,18.976)
                min4=min(min4,18.976)
            if i not in aff_PaperAuthor and len(word2)==0:
                max3=max(max3,18.65)
                min5=min(min5,18.65)
            if i in aff_Author:
                word3=aff_Author[i]
                max2=max(max2,levenshtein.distance(word1,word3))
                min4=min(min4,levenshtein.distance(word1,word3))
            if i in aff_PaperAuthor:
                word4=aff_PaperAuthor[i]
                max3=max(max3,levenshtein.distance(word2,word4))
                min5=min(min5,levenshtein.distance(word2,word4))
            if i not in aff_Author and len(word1)!=0:
                max2=max(max2,levenshtein.distance(word1,word3))
                min4=min(min4,levenshtein.distance(word1,word3))
            if i not in aff_PaperAuthor and len(word2)!=0:
                max3=max(max3,levenshtein.distance(word2,word4))
                min5=min(min5,levenshtein.distance(word2,word4))
    vector=np.append(vector,max2)
    vector=np.append(vector,max3)
    vector=np.append(vector,min4)
    vector=np.append(vector,min5)
    return vector


# In[ ]:



