import math
import numpy as nm
import pandas as pd  
import sklearn
from scipy.stats import pearsonr
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
import matplotlib.pyplot as plt
import warnings

from random import seed
from random import randint
from statistics import NormalDist


k=10
N=10
r=3
p=0.8
'su'
gamma=0.8
'corr'
theta =0.8
'load'
beta=0.9
seed(1)
tfv= list()
tfm= list()
trov= list() 
NFV = list()
NFM = list()
NROV = list()
sz = list()
P = list()



'Randomly generated task requirements, distribution information,' 
'computational capability and size'  

def function(k,N,r):
    
    for i in range(k):
        v=list()
        m=list()
        rov=list()
        for l in range(r):
            if(i%3==0):
                v.append([randint(1,2),randint(3,4)])
                m.append([randint(1,2),randint(3,4)])
                rov.append([randint(1,2),randint(3,4)])
            elif (i%3==1):
                v.append([randint(5,6),randint(7,8)])
                m.append([randint(5,6),randint(7,8)])
                rov.append([randint(5,6),randint(7,8)])
            else:
                v.append([randint(9,10),randint(11,12)])
                m.append([randint(9,10),randint(11,12)])
                rov.append([randint(9,10),randint(11,12)])
        tfv.append(v)
        tfm.append(m)
        trov.append(rov)
    for j in range(N):
        V=list()
        M=list()
        ROV=list()
        for l in range(r):
            if(j%3==0):
                V.append([2.5,0.1])
                M.append([2.5,0.1])
                ROV.append([[2.5,0.1],[2,0.1]])
            elif (j%3==1):
                 V.append([6.5,0.1])
                 M.append([6.5,0.1])
                 ROV.append([[6.5,0.1],[6.5,0.1]])
            else:
                V.append([10.5,0.1])
                M.append([10.5,0.1])
                ROV.append([[10.5,0.1],[10.5,0.1]])
        NFV.append(V)
        NFM.append(M)
        NROV.append(ROV)
    for i in range(k):
        'sz[i] = randint(1,5) '
        sz.append(randint(1,5))
    for j in range(N):
        P.append(randint(50,100))
       
    
    return 
   
function(k,N,r)

"First Come First Served"

def FCFS(k,N,r,p,beta):
    nts1=nm.empty(N)
    ass1=nm.empty(k)
    for i in range(k):
        ass1[i] = -1
    for j in range(N):
        nts1[j] = 0
    for i in range(k):
        for j in range(N):
            if (ass1[i] == -1 and (nts1[j]+sz[i])/P[j] <= beta):
                ass1[i] = j
                nts1[j] = nts1[j] + sz[i]
                break
    return ass1
         
ass1 = FCFS(k,N,r,p,beta)  


'MAX_MIN'
def MM(k,N,r,p,beta):
    nts2=nm.empty(N)
    ass2=nm.empty(k)
    for i in range(k):
        ass2[i] = -1
    for j in range(N):
        nts2[j] = 0
    count5 =0
    while (count5 != k):
        min = 1000
        max = 0
        for i in range(k):
            if(sz[i] > max and ass2[i] == -1):
                max = sz[i]
                index5 = i
            if(sz[i] < min and ass2[i] == -1):
                min = sz[i]
                index6 = i
        for j in range(N):
              if ((nts2[j]+sz[index5])/P[j] <= beta) :
                  ass2[index5] = j
                  nts2[j] = nts2[j] + sz[index5]
                  break
        if ((nts2[j]+sz[index6])/P[j] <= beta):
            ass2[index6] = j
            nts2[j] = nts2[j] + sz[index6]
        else:
            for j in range(N):
                  if ((nts2[j]+sz[index6])/P[j] <= beta ):
                      ass2[index6] = j
                      nts2[j] = nts2[j] + sz[index6]
        count5 = count5 + 1
    return ass2

ass2 = MM(k,N,r,p,beta)  


'Suitability'
def function1(k,N,r,p,gamma):
    su = nm.empty((k,N))
    for i in range(k):
        for j in range(N):
            P = 1
            for l in range(r):
                P1 = p * (NormalDist(mu=NFV[j][l][0],sigma=NFV[j][l][1]).cdf(tfv[i][l][1])-\
                NormalDist(mu=NFV[j][l][0],sigma=NFV[j][l][1]).cdf(tfv[i][l][0])) + 1-p
                    
                P2 = p * (NormalDist(mu=NFM[j][l][0],sigma=NFM[j][l][1]).cdf(tfm[i][l][1])-\
                NormalDist(mu=NFM[j][l][0],sigma=NFM[j][l][1]).cdf(tfm[i][l][0])) + 1-p
                    
                P3 = p * (NormalDist(mu=NROV[j][l][0][0],sigma=NROV[j][l][0][1]).cdf(trov[i][l][1])-\
                NormalDist(mu=NROV[j][l][1][0],sigma=NROV[j][l][1][1]).cdf(trov[i][l][0])) + 1-p
                    
                E = P1*P2*P3
            P = P * E
            if P>=gamma:
                su[i][j]=1
            else:
                su[i][j]=0
    return su
                
su = function1(k,N,r,p,gamma)

'Overlap'
def function2(rq,rw,r):
    ov1=nm.empty(r)
    ov2=nm.empty(r)
    sum1=0
    sum2=0
    for l in range(r):
        ov1[l]= max(0, min(rq[l][1],rw[l][1])-max(rq[l][0],rw[l][0])) / (rq[l][1]-rq[l][0])
        sum1=sum1+ov1[l]
        ov2[l]= max(0, min(rw[l][1],rq[l][1])-max(rw[l][0],rq[l][0])) / (rw[l][1]-rw[l][0])
        sum2=sum2+ov2[l]
    mean1 = sum1/r
    mean2 = sum2/r
    sum3 = 0
    sum4 = 0
    sum5 = 0
    sum6 = 0
    for l in range(r):
        sum6 = sum6 + (ov1[l]+ov2[l])/2
        sum3 = sum3 + (ov1[l]-mean1)*(ov2[l]-mean2)
        sum4 = sum4 + (ov1[l]-mean1)**2
        sum5 = sum5 + (ov2[l]-mean2)**2
    'corr = sum3/(math.sqrt(sum4)*math.sqrt(sum5))'
    sum6 = sum6/r
    return sum6

'Computation of the correlated groups'
def function3(k,theta):
    cg=nm.empty(k)
    current = 0
    for i in range(k):
        cg[i]=-1
    while (-1 in cg):
        for i in range(k):
            if (cg[i] == -1):
                cg[i] = current
                break;
        for j in range(k):
            if (cg[j] == -1):
                a=function2(tfv[i],tfv[j],r)
                b=function2(tfm[i],tfm[j],r)
                c=function2(trov[i],trov[j],r)
                if (a >= theta and b >= theta and c >= theta):
                    cg[j] = current
        current = current +1
     
    l = current 
    cgint=nm.empty((l,N))
    for i in range(l):
        int = nm.empty(N)
        for h in range(N):
            int[h] = 1
        for j in range(k):
            if cg[j] == i :
                for h in range(N):
                    if (int[h]==0 or su[j][h]==0):
                        int[h] = 0
            
        cgint[i] = int
        
    return cg,l,cgint

cg,l,cgint= function3(k,theta)


'Scheduling based on the correlated groups'

def function4(k,N,beta):
    sumcg = 0
    nts = nm.empty(N)
    op = nm.empty(l)
    ncg = nm.empty(N)
    ass = nm.empty(k)
    for i in range(k):
        ass[i]=-1
    for j in range(N):
        nts[j] = 0
        ncg[j] = 0
        for i in range(l):
            if (cgint[i][j] == 1):
                ncg[j] = ncg[j] + 1
    for i in range(l):
        op[i] = sum(cgint[i])
    count1 = sum(op)
    count2 = sum(ncg)
    
    while (count1!=0 and count2!=0):
        
        min = 10000
        for j in range(N):
            if ncg[j] < min and ncg[j]!=0:
                min = ncg[j]
                index1 = j
        
        min = 100000
        
        for i in range(l):
            if (cgint[i][index1]==1):
                if(op[i] < min and op[i]!= 0):
                    min = op[i]
                    index2 = i
        
        for d in range(nm.count_nonzero(cg == index2)):
            
            max = 0 
            for h in range(k):
                if (cg[h] == index2):
                    if(sz[h] > max and ass[h] == -1 ):
                        max = sz[h]
                        index3 = h 
            
            if(max!=0 and nts[index1]+sz[index3])/P[index1] <= beta and ass[index3]==-1:
                ass[index3] = index1
                sumcg = sumcg +1
                
                nts[index1] = nts[index1] + sz[index3]
               
            
            min = 1000 
            for h in range(k):
                if (cg[h] == index2):
                    if(sz[h] < min and ass[h] == -1):
                        min = sz[h]
                        index4 = h 
          
            if(min != 1000):
                if((nts[index1]+sz[index4])/P[index1] <= beta and ass[index4]==-1):
                    ass[index4] = index1
                    sumcg = sumcg +1
                   
                    nts[index1] = nts[index1] + sz[index4]
                    
               
           
        ncg[index1] = ncg[index1] -1
        op[index2] = op[index2] -1
        count1 = sum(op)
        count2 = sum(ncg)
    return ass,cg,op,ncg,nts,sumcg

ass,cg,op,ncg,nts,sumcg= function4(k,N,beta)
print("based on correlation",sumcg/k*100)


def function5(beta):
    count3 = 0
    for i in range(k):
        if ass[i] == -1:
            count3 =count3 +1
    count4 =0
    
    while count4 != count3:
        min = 1000
        max = 0
        for i in range(k):
            if (ass[i]==-1 and sz[i]>max):
                max = sz[i]
                index5 = i
            
            if (ass[i]==-1  and sz[i]<min):
                min = sz[i]
                index6 = i
        for j in range(N):
            if su[index5][j] == 1 and (nts[j]+sz[index5])/P[j] <= beta:
                ass[index5] = j
                'cg[index5] = -1'
                nts[j] = nts[j] + sz[index5]
                
                break;
 
        for j in range(N):
            if su[index6][j] == 1 and (nts[j]+sz[index6])/P[j] <= beta:
                ass[index6] = j
                'cg[index6] = -1'
                nts[j] = nts[j] + sz[index6]
                
                break;
        count4 = count4 + 1
    return count4

count4 = function5(beta)


ass=ass.astype(int)
ass1=ass1.astype(int)
ass2=ass2.astype(int)

"TASK FAILURE"

tf=0
tf1=0
tf2=0
for i in range(k):
    if su[i][ass[i]]==0:
        tf = tf + 1
    if su[i][ass1[i]]==0:
        tf1 = tf1 + 1
    if su[i][ass2[i]]==0:
        tf2 = tf2 + 1
print("Task Failure",tf1/k*100,tf2/k*100,tf/k*100)   
     


