"""
publications is a dictionary, for each publication it contains its vector
this function returns a dictionary which contains for each publication its cluster number 0 or 1
"""
def dist(list1,list2):
    n=len(list1)
    distance=0.0
    for i in range(n):
        diff=float(list1[i]-list2[i])
        distance=distance+(diff*diff)
    return distance


def twomeans(publications,max_no_of_iterations):
    keyset=list(publications.keys())
    no_of_publications=len(keyset)
    dim=len(publications[keyset[0]])
    mx=-1
    clut1=0
    clut1=1
    for i in range(no_of_publications):
        for j in range(i+1,no_of_publications):
            d = dist(publications[keyset[i]],publications[keyset[j]])>mx
            if d>mx:
                mx=d
                clut1=i
                clut2=j
    clusters=[]
    for i in range(no_of_publications):
        if dist(publications[keyset[i]],clut1)<dist(publications[keyset[i]],clut1):
            clusters.append(0)
        else:
            clusters.append(1)
    for iters in range(max_no_of_iterations):
        clut_vector = [[0.0 for _ in range(dim)] for _ in range(2)]
        count = [0.0 for _ in range(2)]
        for i in range(no_of_publications):
            for j in range(dim):
                clut_vector[clusters[i]][j] = clut_vector[clusters[i][j]] + publications[keyset[i]][j]
            count[clusters[i]] = count[clusters[i]] + 1.0
        for i in range(dim):
            clut_vector[0][i] = clut_vector[0][i] / count[0]
            clut_vector[1][i] = clut_vector[1][i] / count[1]
        for i in range(no_of_publications):
            if dist(publications[keyset[i]],clut_vector[0])< dist(publications[keyset[i]],clut_vector[1]):
                clusters[i]=0
            else:
                clusters[j]=1

    ret={}
    for i in range(no_of_publications):
        ret[keyset[i]]=clusters[i]
    return ret

