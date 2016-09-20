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

    def create(self):
        #creates dicts of words objects keyed with word name
        for w,y in self.dic.items():
           for words in y:
                if words in self.wrds:
                    self.wrds[words].add(w)
                else:
                    self.wrds[words] = word()
                    self.wrds[words].add(w)


    def calculate(self,doc,word):
        #returns the tf-idf score of word in doc
        return((0.5+0.5*(self.wrds[word].count(doc))/len(self.dic[doc]))*((math.log(len(self.dic.keys())))/(self.wrds[word].No_authors())))




























































































































































































































































































    
