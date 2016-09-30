import kmeans
import vecfeature
import levenshtein
from operator import itemgetter

"""
w1,w2 are strings and returns a boolean
"""
def score_of_words(w1,w2):
    dist = levenshtein.distance(w1,w2)
    len1=len(w1)
    len2=len(w2)
    if(len1==0 or len2==0):
        return 0
    if dist<=4 and float(dist)/float(max(len1,len2)) <= 0.4:
        return 1
    return 0
"""
returns score of list l1, l2 each element of list is a list of two arguments word,tfidf
"""
def score_of_lists(l1,l2):
    ret=0.0
    len1=len(l1)
    len2=len(l2)
    for i in range(len1):
        for j in range(len2):
            if score_of_words(l1[i][0],l2[j][0]) == 1 :
                ret = ret + l1[i][1]*l2[j][1]
    return ret


"""
this function returns a list of tuples: [publication,score,cluster_number]
aKw is keywords of author clusters is the dictionary containing the cluster_number
tkw is the dictionary
"""
def cluster_matching_words(aKw,tkw,clusters):
    keyset = list(clusters.keys())
    no_of_publication = len(keyset)
    ret = [ ]
    for i in range(no_of_publication):
        paper = keyset[i]
        list_words = tkw[paper]
        score = score_of_lists(list_words,aKw)
        cluster_number = clusters[paper]
        ret.append((paper,score,cluster_number))
    return  ret

"""
the function sorts the list and returns the sorted list according to the second parameter in reverse order
"""
def sort_list(final_list):
    final_list=sorted(final_list,key=itemgetter(1))
    final_list[:]=final_list[::-1]
    # for i in range(l):
    #     for j in range(i+1,l):
    #         if final_list[i][1] < final_list[j][1]:
    #             swap(final_list[i],final_list[j])
    return final_list
"""
the function returns the cluster number of the cluster which mathces more with the author
"""
def nearest_cluster(lis):
    l=len(lis)
    count=[ 0,0]
    total_score= [ 0.0, 0,0]
    for i in range(l):
        count[lis[i][2]]=count[lis[i][2]]+1
        total_score[lis[i][2]]=total_score[lis[i][2]]+lis[i][1]
    if count[0]==0:
        return 1
    if count[1]==0:
        return 0
    if float(total_score[1])/float(count[1]) > float(total_score[0])/float(count[0]):
        return 1
    return 0
"""
the function returns a permutation of publications in its probable order 
aKw is a list of tuples, each list containing word, its tf-idf score of author's keywords
tkw is a dictionary  {paper: list of (keywords,tf-idf score) }
"""
def unsupervised(aaKw,kWp,aP,jKw,PJ,A,T,author_id, confirmed, publications, aKw ,tkw ):
    ambiguos_publications=[]
    for paper in publications:
        if paper not in confirmed:
            ambiguos_publications.append(paper)
    dct={}
    for paper in ambiguos_publications:
        dct[paper] = vecfeature.vec(paper,author_id,aaKw,kWp,aP,jKw,PJ,A,T)
    clusters = kmeans.twomeans(dct,100)
    # print ("dct",dct)
    # print ("clusters",clusters)
    final_list = cluster_matching_words(aKw,tkw,clusters)
    # print ("fl",final_list)
    sorted_list = sort_list(final_list)
    # print ("sl",sorted_list)
    ret=[]
    # print ("confirmed",confirmed)
    # print ("publications",publications)
    for paper in publications:
        if paper in confirmed:
            ret.append(paper)
    l = len(sorted_list)
    nc = nearest_cluster(sorted_list)
    # print ("nc",nc)
    for i in range(l):
        if sorted_list[i][2] == nc:
            ret.append(sorted_list[i][0])
    for i in range(l):
        if sorted_list[i][2] == 1-nc:
            ret.append(sorted_list[i][0])
    return ret
    
