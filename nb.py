import vecfeature
import pickle as pi
import tfidf
import numpy as np
import math
import unsupervised

# Go through the authors' confirmed publications. If a particular keyword of author appears, increase tf-idf of that keyword that to sum1. If a particular keyword of author doesn't appear, increase tf-idf of that keyword to sum2. Use sum1 and sum2 (and count1 and count2) to compute mean and sd of first 16 features. Same mean and sd for next 8 features. Compute mean and sd of overlapping publications that author has with other authors for 3rd feature. 

def gaussian(x,myu,sigma):
    c=math.log(1/math.sqrt(2.0*sigma*sigma*math.pi))+(-((x-myu)*(x-myu)/(2.0*sigma*sigma)))
    return (c)
def NB(arg1,arg2,arg3,arg4,aKw,kWp,aP,jKw,PJ,A,A_list,T,paperIDs,authorID):
    parameters=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0],[0,0]]
    # aKw=pi.load(open("aKw.p","rb"))
    # print ("aKw")
    # kWp=pi.load(open("kWp.p","rb"))
    # print ("kWp")
    # aP=pi.load(open("aP1.p","rb"))
    # print ("aP")
    # jKw=pi.load(open("jKw.p","rb"))
    # print ("jKw")
    # PJ=pi.load(open("PJ.p","rb"))
    # print ("PJ")
    # A=pi.load(open("A.p","rb"))
    # print ("A")
    # A_list=pi.load(open("A_list.p","rb"))
    # print ("A_list")
    # T=tfidf.tfidf("aKw.p")
    # args=[]
    # for i in aP:
    #     args.append(i)
    # T.create(args)
    # print ("TF-IDF Done")
    confirmedPublications=[]
    keywordsAuthor=[]
    if authorID in aP:
        confirmedPublications=aP[authorID]
    if authorID in aKw:
        keywordsAuthor=aKw[authorID]
    temp=len(confirmedPublications)

    tfidfvals_pos=np.empty(len(keywordsAuthor)*len(confirmedPublications))
    tfidfvals_neg=np.empty(len(keywordsAuthor)*len(confirmedPublications))
    cnt1=cnt2=0

    overpub_pos=np.empty(len(A_list)-1)
    overpub_neg=np.empty(len(A_list)-1)
    #Mean of positive and negative for first feature. 
    for i in confirmedPublications:
        for j in keywordsAuthor:
            if i in kWp and j in kWp[i] and len(j)>0:
                tfidfvals_pos[cnt1]=T.calculate(authorID,j)
                cnt1+=1
            elif len(j)>0:
                tfidfvals_neg[cnt2]=T.calculate(authorID,j)
                cnt2+=1
    tfidfvals_pos=np.resize(tfidfvals_pos,cnt1)
    tfidfvals_neg=np.resize(tfidfvals_neg,cnt2)
    if(len(tfidfvals_pos)>0): 
        parameters[0][0]=np.mean(tfidfvals_pos)
        parameters[0][1]=np.std(tfidfvals_pos)
    if(len(tfidfvals_neg)>0): 
        parameters[0][2]=np.mean(tfidfvals_neg)
        parameters[0][3]=np.std(tfidfvals_neg)
    #Mean of positive and negative for second feature same as first feature. 
    parameters[1]=parameters[0]
    print ("Mean of first and second done.")
    #Mean of positive and negative for third feature. 
    j=0
    for i in A_list:
        if i==authorID: continue
        if i in aP:
            overpub_pos[j]=len(set(aP[i]).intersection(set(confirmedPublications)))
            overpub_neg[j]=len(set(confirmedPublications))-len(set(aP[i]).intersection(set(confirmedPublications)))
        else:
            overpub_pos[j]=0
            overpub_neg[j]=len(set(confirmedPublications))
        j+=1
    overpub_pos=np.resize(overpub_pos,j)
    overpub_neg=np.resize(overpub_neg,j)
    if(len(overpub_pos)>0):
        parameters[2][0]=np.mean(overpub_pos)
        parameters[2][1]=np.std(overpub_pos)
    if(len(overpub_neg)>0):
        parameters[2][2]=np.mean(overpub_neg)
        parameters[2][3]=np.std(overpub_neg)
    print ("Mean of third done.")
    #Mean of positive for fourth feature
    # keywrds=np.empty(len(aKw))
    # j=0
    # for i in aKw:
    #     keywrds[j]=len(aKw[i])
    #     j+=1
    parameters[3][0]=arg1
    parameters[3][1]=arg2
    print ("Mean of fourth done.")
    #Mean of positive for fifth feature
    # keywrds=np.empty(len(kWp))
    # j=0
    # for i in kWp:
    #     keywrds[j]=len(kWp[i])
    #     j+=1
    parameters[4][0]=arg3
    parameters[4][1]=arg4
    print ("Mean of fifth done.")
    ans_prob=np.zeros((len(paperIDs),2))
    ans=np.zeros(len(paperIDs))
    for i in range(0,len(paperIDs)):
        ans_prob[i][1]=paperIDs[i]
    for i in range (0,len(ans_prob)):
        if authorID in aP:
            if ans_prob[i][1] in aP[authorID]:
                ans_prob[i][0]=1
    for i in range(0,len(paperIDs)):
        if ans_prob[i][0]==1: continue
        t_vect=vecfeature.vec(paperIDs[i],authorID,aKw,kWp,aP,jKw,PJ,A,T,1)
        ans_t=0
        if(parameters[0][1]!=0):
            for j in range(0,16):
                ans_t=ans_t+gaussian(t_vect[j],parameters[0][0],parameters[0][1])
        if(parameters[0][3]!=0):
            for j in range(16,32):
                ans_t=ans_t+gaussian(t_vect[j],parameters[0][2],parameters[0][3])
        if(parameters[1][1]!=0):
            for j in range(32,40):
                ans_t=ans_t+gaussian(t_vect[j],parameters[1][0],parameters[1][1])
        if(parameters[1][3]!=0):
            for j in range(40,48):
                ans_t=ans_t+gaussian(t_vect[j],parameters[1][2],parameters[1][3])
        if(parameters[2][1]!=0):
            for j in range(48,52):
                ans_t=ans_t+gaussian(t_vect[j],parameters[2][0],parameters[2][1])
        if(parameters[2][3]!=0):
            for j in range(52,56):
                ans_t=ans_t+gaussian(t_vect[j],parameters[2][2],parameters[2][3])
        if(parameters[3][1]!=0):
            ans_t=ans_t+gaussian(t_vect[56],parameters[3][0],parameters[3][1])
        if(parameters[4][1]!=0):
            ans_t=ans_t+gaussian(t_vect[57],parameters[4][0],parameters[4][1])
        ans_prob[i][0]=ans_t
    ans_prob=sorted(ans_prob, key=lambda row: row[0])
    ans_prob[:]=ans_prob[::-1]
    return (ans_prob)
def NB_main(input1):
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
    A_list=pi.load(open("A_list.p","rb"))
    print ("A_list")
    T=tfidf.tfidf("aKw.p")
    args=[]
    for i in aP:
        args.append(i)
    T.create(args)
    print ("TF-IDF Done")
    keywrds=np.empty(len(aKw))
    j=0
    for i in aKw:
        keywrds[j]=len(aKw[i])
        j+=1
    arg1=np.mean(keywrds)
    arg2=np.std(keywrds)
    print ("args1 done")
    keywrds=np.empty(len(kWp))
    j=0
    for i in kWp:
        keywrds[j]=len(kWp[i])
        j+=1
    arg3=np.mean(keywrds)
    arg4=np.std(keywrds)
    print ("args2 done")
    f=open("output.csv","w")
    f.write("AuthorId,PaperIds")
    f.write("\n")
    no=0
    for i in input1:
        ret=NB(arg1,arg2,arg3,arg4,aKw,kWp,aP,jKw,PJ,A,A_list,T,i[0],i[1])
        f.write(str(i[1]))
        f.write(",")
        for j in ret:
            f.write(str(int(j[1])))
            f.write(" ")
        f.write("\n")
        no+=1
        print (no)
    f.close()
