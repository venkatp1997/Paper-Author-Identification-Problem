import extractor as ex
import pickle as pi

kWp=ex.keywords_Paper("dataRev2/Paper.csv")
pi.dump(kWp,open("kWp.p","wb"))

aP=ex.authors_Paper("confirmedAuthors.csv")
pi.dump(aP,open("aP1.p","wb"))

aKw=ex.authors_keywords(aP, kWp)
pi.dump(aKw,open("aKw.p","wb"))

jKw=ex.journal_keywords(kWp,"dataRev2/Paper.csv")
pi.dump(aKw,open("jKw.p","wb"))

PJ=ex.paper_journal("dataRev2/Paper.csv")
pi.dump(PJ,open("PJ.p","wb"))

A=dict()
for i in aP:
    for j in aP[i]:
        if j not in A: A[j]=[]
        A[j].append(i)

pi.dump(A,open("A.p","wb"))

