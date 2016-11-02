import sys
import nb
import unsupervised
import pickle as pi
import pandas as pd
import tfidf
import rfsvm

if len(sys.argv)<2:
    print ("Incorrect Format")
elif sys.argv[1]=='0':
    data=pd.read_csv("/home/venkat/Downloads/Test.csv")
    input1=[]
    for (index,i) in data.iterrows():
        in1=i["PaperIds"].split()
        in1=[int(i) for i in in1]
        in2=int(i["AuthorId"])
        input1.append((in1,in2))
    nb.NB_main(input1)
elif sys.argv[1]=='1':
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
    # args1=[]
    # args2={}
    # for i in aKw[authorID]:
    #     args1.append((i,T.calculate(authorID,i)))
    # print ("Args-1 Done")
    # for i in paperIDs:
    #     args2[i]=[]
    #     for j in kWp[str(i)]:
    #         args2[i].append((j,T.calculate(authorID,j)))
    # print ("Args-2 Done")
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
    no=0
    for i in input1:
        args1=[]
        args2={}
        authorID=i[1]
        paperIDs=i[0]
        if authorID in aKw:
            for j in aKw[authorID]:
                args1.append((j,T.calculate(authorID,j)))
        print ("Args-1 Done")
        for j in paperIDs:
            args2[j]=[]
            if str(j) in kWp:
                for k in kWp[str(j)]:
                    args2[j].append((k,T.calculate(authorID,k)))
        print ("Args-2 Done")
        if authorID in aP:
            ret=(unsupervised.unsupervised(aKw,kWp,aP,jKw,PJ,A,T,authorID,aP[authorID],paperIDs,args1,args2))
        else:
            ret=(unsupervised.unsupervised(aKw,kWp,aP,jKw,PJ,A,T,authorID,[],paperIDs,args1,args2))
        f.write(str(authorID))
        f.write(",")
        for j in ret:
            f.write(str(j))
            f.write(" ")
        f.write("\n")
        no+=1
        print (no)
    f.close()
elif sys.argv[1]=='2':
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
    authorID=731
    paperIDs=[24943, 688974, 964345, 1201905, 1267992, 1298546, 2180622]
    paperIDs=[str(i) for i in paperIDs]
    args1=[]
    args2={}
    if authorID in aKw:
        for j in aKw[authorID]:
            args1.append((j,T.calculate(authorID,j)))
    print ("Args-1 Done")
    for j in paperIDs:
        args2[j]=[]
        if str(j) in kWp:
            for k in kWp[str(j)]:
                args2[j].append((k,T.calculate(authorID,k)))
    print ("Args-2 Done")
    rfsvm.random_forest(authorID,paperIDs,aP,aKw,kWp,jKw,PJ,A,T,args1,args2)
else:
    print ("Incorrect Format")
