import pickle as pi
import tfidf
import numpy as np

def matching_keywords_pa(aKw,kWp,paperID,authorID):
    # aKw=pi.load(open("aKw.p","rb"))
    # kWp=pi.load(open("kWp.p","rb"))
    if(authorID not in aKw or str(paperID) not in kWp): return set()
    # print ("Hi1")
    # print (authorID,aKw[authorID],kWp[str(paperID)])
    return set(aKw[authorID]).intersection(set(kWp[str(paperID)]))

def matching_keywords_pa_neg(aKw,kWp,paperID,authorID):
    # aKw=pi.load(open("aKw.p","rb"))
    # kWp=pi.load(open("kWp.p","rb"))
    if(authorID not in aKw or str(paperID) not in kWp): ret={} 
    else: ret=set(aKw[authorID]).intersection(set(kWp[str(paperID)]))
    ret1=[]
    if authorID not in aKw: return {}
    for i in aKw[authorID]:
        if i not in ret:
            ret1.append(i)
    return ret1

def matching_keywords_aj(aKw,jKw,journalID,authorID):
    # aKw=pi.load(open("aKw.p","rb"))
    # jKw=pi.load(open("jKw.p","rb"))
    if(authorID not in aKw or journalID not in jKw): return set()
    # print ("Hi2")
    # print (authorID,aKw[authorID],jKw[journalID])
    return set(aKw[authorID]).intersection(set(jKw[journalID]))

def matching_keywords_aj_neg(aKw,jKw,journalID,authorID):
    # aKw=pi.load(open("aKw.p","rb"))
    # jKw=pi.load(open("jKw.p","rb"))
    if(authorID not in aKw or journalID not in jKw): ret={}
    else: ret=set(aKw[authorID]).intersection(set(jKw[journalID]))
    ret1=[]
    if authorID not in aKw: return {}
    for i in aKw[authorID]:
        if i not in ret:
            ret1.append(i)
    return ret1

def matching_papers(aP,authorID1,authorID2):
    # aP=pi.load(open("aP1.p","rb"))
    if(authorID1 not in aP or authorID2 not in aP): return 0
    return len(set(aP[authorID1]).intersection(set(aP[authorID2])))

def matching_papers_neg(aP,authorID1,authorID2):
    # aP=pi.load(open("aP1.p","rb"))
    if(authorID1 not in aP or authorID2 not in aP): 
        if authorID1 not in aP: return 0
        return len(set(aP[authorID1]))
    # print (len(set(aP[authorID1])),len(set(aP[authorID2])),len(set(aP[authorID1]))-len(set(aP[authorID1]).intersection(set(aP[authorID2]))))
    return len(set(aP[authorID1]))-len(set(aP[authorID1]).intersection(set(aP[authorID2])))

def get_journal(PJ,paperID):
    # PJ=pi.load(open("PJ.p","rb"))
    if paperID not in PJ: return 0
    return PJ[paperID]

def get_authors(A,paperID):
    # A=pi.load(open("A.p","rb"))
    if paperID not in A: return []
    return (A[paperID])

def noKeywords_Author(aKw,authorID):
    # aKw=pi.load(open("aKw.p","rb"))
    if authorID not in aKw: return 0
    cnt=0
    for i in aKw[authorID]:
        if len(i)>0:
            cnt+=1
    return cnt

def noKeywords_Paper(kWp,paperID):
    # kWp=pi.load(open("kWp.p","rb"))
    if paperID not in kWp: return 0
    cnt=0
    for i in kWp[str(paperID)]:
        if len(i)>0:
            cnt+=1
    return cnt

def vec(paperID,authorID,aKw,kWp,aP,jKw,PJ,A,T,nb_flag=0):
    vector=np.empty(0)
    #Feature-1
    ret=matching_keywords_pa(aKw,kWp,paperID,authorID)
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
        if(j>=16): break
    for k in range(j,16):
        vector=np.append(vector,0)
    if(nb_flag==1):
        #Feature-1_neg
        ret=matching_keywords_pa_neg(aKw,kWp,paperID,authorID)
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
            if(j>=16): break
        for k in range(j,16):
            vector=np.append(vector,0)

    journalID=get_journal(PJ,paperID)
    # print ("Feature-1 Done")
    #Feature-2
    ret=matching_keywords_aj(aKw,jKw,journalID,authorID)
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
        if(j>=8): break
    for k in range(j,8):
        vector=np.append(vector,0)
    # print ("Feature-2 Done")
    if(nb_flag==1):
        #Feature-2_neg
        ret=matching_keywords_aj_neg(aKw,jKw,journalID,authorID)
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
    ret=get_authors(A,paperID)
    temp=np.zeros(50000)
    cnt=0
    for i in ret:
        if i==authorID: continue
        temp[cnt]=matching_papers(aP,i,authorID)
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
        ret=get_authors(A,paperID)
        temp=np.zeros(50000)
        cnt=0
        for i in ret:
            if i==authorID: continue
            temp[cnt]=matching_papers_neg(aP,i,authorID)
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
    vector=np.append(vector,noKeywords_Author(aKw,authorID))
    # print ("Feature-4 Done")
    #Feature 5
    vector=np.append(vector,noKeywords_Paper(kWp,paperID))
    # print ("Feature-5 Done")
    return vector

