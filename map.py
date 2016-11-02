from sklearn.metrics import average_precision_score
import pandas as pd
import numpy as np

true=pd.read_csv("True.csv")
out=pd.read_csv("Out.csv")

sum1=0
for j in range(true.shape[0]):
    x=[int(i) for i in true.iloc[j]['PaperIds'].split()]
    y=[int(i) for i in out.iloc[j]['PaperIds'].split()]
    x=np.array(x)
    y=np.array(y)
    print (x,y)
    sum1+=average_precision_score(x,y)
print (float(sum1)/float(true.shape[0]))

