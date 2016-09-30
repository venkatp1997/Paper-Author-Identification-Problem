import math
import csv 
import re
import pandas as pd
import pickle as pi
class word:
    def __init__(self):
        self.D = {}



    def add(self,doc):
        if doc in self.D:
            self.D[doc] += 1
        else:
            self.D[doc] = 1

    def count(self,doc):
        if doc in self.D:
            return(self.D[doc])
        else:
            return(0)
    def No_authors(self):
        return(len(self.D.keys()))
    
class tfidf:
    def __init__(self,f):
        fl = open(f,'rb')
        D = pi.load(fl)
        self.dic = D
        self.wrds = {}
        self.num_doc = len(self.dic.keys())
        self.list=[]
        self.max={}

    def create(self,authorIDs):
        #creates dicts of words objects keyed with word name

        for w in authorIDs:
            if w not in self.dic: continue
            mx = 1
            cnt = {}
            for words in self.dic[w]:
                if words not in cnt:
                    cnt[words] = 1
                else:
                    cnt[words] += 1
                    mx = max(mx,cnt[words])
            self.max[w] = mx




        for w in authorIDs:
            if w not in self.dic: continue
            for words in self.dic[w]:
                if words in self.wrds:
                    self.wrds[words].add(w)
                else:
                    self.wrds[words]=word()
                    self.wrds[words].add(w)
        # for w,y in self.dic.items():
        #    if w not in authorIDs: continue
        #    for words in y:
        #        if words in self.wrds:
        #            self.wrds[words].add(w)
        #        else:
        #            self.wrds[words] = word()
        #            self.wrds[words].add(w)

    def calculate(self,doc,word):
        #returns the tf-idf score of word in doc
        if word not in self.wrds: return 0
        if doc not in self.max: return 0
        return((0.5+0.5*(float(self.wrds[word].count(doc)))/float(self.max[doc]))*((math.log(float(len(self.dic.keys()))))/float((self.wrds[word].No_authors()))))
