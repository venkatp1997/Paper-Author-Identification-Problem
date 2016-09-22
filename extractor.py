"""
Contains functions to handle data. 
Extracts and removes noise, ultimately to give {authors: keywords} relation.

"""
import re
import pandas as pd
from collections import Counter
import pickle as pi
import tfidf 

def second_names(x):
    if x: return x.split()[-1]
    else: return ''

def filter_authors(probable_authors):
    """ Returns filtered list of authors """
    #second_names = lambda x: x.split()[-1]
    names, ids = zip(*probable_authors)
    cleaned = []
    counter = Counter(list(map(second_names, names)))
    for (name, aid) in probable_authors:
        if counter[second_names(name)] == 1:
            cleaned.append((name, aid))
    return cleaned



def squeeze(aid_aname_papers):
    id_name = {}
    id_papers = {}
    paper_authors = {}

    # Create list of authors for each paper
    # {key: value} = {pid: (name, aid)}
    print("Creating list of authors for paper..")
    for (pid, aid, name) in aid_aname_papers:
        if pid not in paper_authors.keys():
            paper_authors[pid] = []
        paper_authors[pid].append((name, aid))

    #print(paper_authors)
    # Filter authors for paper, noise
    print("Filtering to remove noise...")
    for pid in paper_authors:
        paper_authors[pid] = filter_authors(paper_authors[pid])

    # After filtering, create required relation
    print("Creating required relation...")
    for pid in paper_authors:
        for (aname, aid) in paper_authors[pid]:
            if aid not in id_papers.keys():
                id_papers[aid] = []
                id_name[aid] = aname
            id_papers[aid].append(pid)

    gentuple = lambda x: (x, id_name[x], id_papers[x])
    return map(gentuple, id_name.keys())

def export(authors, outputfile):
    # TODO add header rows.
    print("Opening file to writeout...")
    with open(outputfile, 'w+') as fp:
        data = pd.DataFrame.from_records(authors)
        data.to_csv(authors)


def Authors():
    print("Loading data...")
    data = pd.read_csv('dataRev2/PaperAuthor.csv', delimiter=',', header=0)
    data.fillna('', inplace=True)
    print("Loaded data...")
    aid_aname_papers = zip(data["PaperId"], data["AuthorId"], data["Name"])

    print("Squeezing authors...")
    return squeeze(aid_aname_papers)


def keywords_Paper(paperfile):
    """ Reads csv, returns dict{ paper_id: keywords} """
    data = pd.read_csv(paperfile, delimiter=',', header=0)
    data.fillna('', inplace=True)
    data["Keyword"]=[i.lower() for i in data["Keyword"]]
    cleanKeyword = lambda x: re.split(':|;|,|\|| ', x)
    strdata = map(str,data["Id"])
    pid_keywords = zip(strdata, map(cleanKeyword, data["Keyword"]))

    return dict(pid_keywords)

def authors_Paper(authorfile):
    """ Reads csv, returns [(author_id, [paper_ids])]"""
    data = pd.read_csv(authorfile, delimiter=',', header=0)
    data.fillna('', inplace=True)
    translator = str.maketrans({key:None for key in '\'\"[] '})
    extractPapers = lambda x: x.translate(translator).split(',')
    aid_pids = zip(data["author_id"], map(extractPapers, data["paper_ids"]))
    return dict(aid_pids)

def authors_keywords(auth_paper, keyword_paper):
   """ Reads dicts, creates new relation: {author:keyword} """
   # getKeywords = lambda paper_id: keyword_paper[int(paper_id)]
   # getAuthorKeywords = lambda x: (x[0], list(map(getKeywords, x[1])))
   # auth_kwds = list(map(getAuthorKeywords, auth_paper))
   auth_kwds = {}
   for x in auth_paper:
       for paper in x[1]:
           if paper in keyword_paper:
               for wd in keyword_paper[paper]:

                    if x[0] in auth_kwds:
                        auth_kwds[x[0]].append(wd)
                    else:
                        auth_kwds[x[0]] = []
                        auth_kwds[x[0]].append(wd)
   return auth_kwds

def noisy_authors():
    print("Loading data...")
    data = pd.read_csv('dataRev2/PaperAuthor.csv', delimiter=',', header=0)
    data.fillna('', inplace=True)
    print("Loaded data...")
    aid_aname_papers = zip(data["PaperId"], data["AuthorId"])
    return list(aid_aname_papers)

def journal_keywords(keyword_paper,papers):
    """ Returns a dict where the key is JournalId and the value is the list of keywords assosciated with all the papers published in that journal. """
    data = pd.read_csv(papers, delimiter=',', header=0)
    data.fillna('', inplace=True)
    translator = str.maketrans({key:None for key in '\'\"[] '})
    # extractPapers = lambda x: x.translate(translator).split(',')
    aid_pids = zip(data["JournalId"],data["Id"])
    jKw=list(aid_pids)
    kWd={}
    for (i,j) in jKw:
        if i not in kWd:
            kWd[i]=[]
        j=str(j)
        if j not in keyword_paper: continue
        for w in keyword_paper[j]:
            kWd[i].append(w.lower())
    return kWd

def paper_journal(papers):
    data = pd.read_csv(papers, delimiter=',', header=0)
    data.fillna('', inplace=True)
    translator = str.maketrans({key:None for key in '\'\"[] '})
    # extractPapers = lambda x: x.translate(translator).split(',')
    aid_pids = zip(data["Id"],data["JournalId"])
    return dict(aid_pids)

def matching_keywords(author_id,paper_id):
    return set(aKw[author_id]).intersection(set(kwP[paper_id]))

if __name__ == '__main__':
    # ret=noisy_authors()
    # AuthorDict=dict()
    # for i in ret:
    #     if i[0] not in AuthorDict: AuthorDict[i[0]]=[]
    #     AuthorDict[i[0]].append(i[1])
    # pi.dump(AuthorDict,open("A.p","wb"))
    # for i in ret:
    #     for j in i[2]:
    #         if j not in AuthorDict: AuthorDict[j]=[]
    #         AuthorDict[j].append(i[0])
    #         if(j==3): print (i[2])
    # pi.dump(AuthorDict,open("A.p","wb"))
    # temp=(paper_journal("dataRev2/Paper.csv"))
    # pi.dump(temp,open("PJ.p","wb"))
    #records = Authors('dataRev2/PaperAuthor.csv')
    #exportConfirmedAuthor(records, "confirmedAuthor.csv")
    # global kwP,aP,aKw
    # kwP = keywords_Paper("dataRev2/Paper.csv")
    # pi.dump(kwP,open("kWp.p","wb"))
    # print(" keywords of papers : DONE")
    # aP = authors_Paper("confirmedAuthors.csv")
    # pi.dump(aP,open("aP1.p","wb"))
    # print(" authors of papers : DONE")
    # aKw = authors_keywords(aP, kwP)
    # pi.dump(aKw,open("aKw.p","wb"))
    # print(" Keyword of authors : DONE")
    # T=tfidf.tfidf("keywrd.p")
    # T.create()
    # jKw=journal_keywords(kwP,"dataRev2/Paper.csv")
    # pi.dump(aKw,open("jKw.p","wb"))
    # f=open('dataRev2/journalKeywords','wb')
    # pi.dump(jKw,f)

    #1
    # for i in aKw:
    #     for j in kwP:
    #         ret=matching_keywords(i,j)
    #         print (aKw[i])
    #         print (-1)
    #         print (kwP[j])
    #         print (-2)
    #         print (ret)
    #         # for k in ret:
    #         #     print (k,T.calculate(i,k))
    #         n=input()
    #     n=input()
