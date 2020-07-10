# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 08:58:50 2020

@author: abazin
"""

# ========================= Modules ===========================
import numpy as np
from matplotlib import pyplot as plt
from time import perf_counter
from xlwt import Workbook
import copy
from multiprocessing import Pool
import itertools
from collections import Counter
import warnings
from itertools import chain
import matplotlib.pyplot as plt
import math
# =============================================================================





'''
Loading functions
'''

#loads a rankings file
#each line contains the comma-separated rankings of an alternative by the criteria (columns)
def loadRankings(f):
    file = open(f,"r")
    R = []
    for line in file:
        row = line.split("\n")[0]
        row = row.split(",")
        R.append(list(row))
    file.close()
    return np.array(R).astype(int)



#loads knowledge about the criteria
#each line is a comma-separated list of terms describing a criterion (line i = criterion i)
def loadKnowledgeCriteria(f):
    file = open(f,"r")
    R = []
    for line in file:
        row = line.split("\n")[0]
        row = row.split(",")
        R.append(list(row))
    file.close()
    return R     
      

#load a knowledge base
#each line is an implication between a premisse and a conclusion separated by a semicolon
#the premisses and conclusions are comma-separated lists of terms
def loadKnowledgeBase(f):
    file = open(f,"r")
    R = []
    for line in file:
        row = line.split("\n")[0]
        row = row.split(";")
        premisse = row[0].split(",")
        conclusion = row[1].split(",")
        R.append([list(premisse),list(conclusion)])
    file.close()
    return R
    
    

'''
Set manipulation functions
'''

#Does A contain B ?
def contains(A, B):
    T = True
    for b in B:
        if not b in A:
            T = False
            break
    return T


#A \cup B
def union(A,B):
    S = A.copy()
    for b in B:
        if not b in S:
            S = S+[b]
    return S


#A \cap B
def intersect(A,B):
    return [a for a in A if a in B]


#A\B
def diff(A,B):
    return [a for a in A if a not in B]



#Logical / transitive closure of a set by a set of implication rules
def logicalClosure(Set,Rules):
    S = Set.copy()
    fin = False    
    while not fin:
        s = len(S)
        for I in Rules:
            if contains(S,I[0]):
                S = union(S,I[1])
        if len(S) == s:
            fin = True         
    return S

                

'''
Aggregation functions
'''

#Returns the Pareto front of the multicriteria decision problem given by rankings of alternatives 
def Pareto(ranks):
    ranks = np.array(ranks).astype(int)
    # Count number of items
    population_size = ranks.shape[0]
    # Create a NumPy index for ranks on the pareto front (zero indexed)
    population_ids = np.arange(population_size)
    # Create a starting list of items on the Pareto front
    # All items start off as being labelled as on the Pareto front
    pareto_front = np.ones(population_size, dtype=bool)
    # Loop through each item. This will then be compared with all other items
    for i in range(population_size):
        # Loop through all other items
        for j in range(population_size):
            # Check if our 'i' pint is dominated by out 'j' point
            if all(ranks[j] <= ranks[i]) and any(ranks[j] < ranks[i]):
                # j dominates i. Label 'i' point as not on Pareto front
                pareto_front[i] = 0
                # Stop further comparisons with 'i' (no more comparisons needed)
                break
    # Return ids of scenarios on pareto front
    return population_ids[pareto_front]    


#Returns the top-"depth" alternatives in the partially ordered set induced by the Pareto dominance 
def ParetoDepth(ranks,depth):
    R = np.array([])
    nrank = copy.deepcopy(ranks)
    
    for d in range(depth):
        P = ParetoDepth2(nrank,R)
        for p in P:
            R = np.array(list(R)+[p])
            np.delete(nrank,p,0)
        print(R)
        
    return R

def ParetoDepth2(ranks, known):
    ranks = np.array(ranks).astype(int)
    # Count number of items
    population_size = ranks.shape[0]
    # Create a NumPy index for ranks on the pareto front (zero indexed)
    population_ids = np.arange(population_size)
    # Create a starting list of items on the Pareto front
    # All items start off as being labelled as on the Pareto front
    pareto_front = np.ones(population_size, dtype=bool)
    
    for k in known:
        pareto_front[k] = 0
    
    # Loop through each item. This will then be compared with all other items
    for i in range(population_size):
        if i not in known:
            # Loop through all other items
            for j in range(population_size):
                if j not in known:
                    # Check if our 'i' pint is dominated by out 'j' point
                    if all(ranks[j] <= ranks[i]) and any(ranks[j] < ranks[i]):
                        # j dominates i. Label 'i' point as not on Pareto front
                        pareto_front[i] = 0
                        # Stop further comparisons with 'i' (no more comparisons needed)
                        break
    # Return ids of scenarios on pareto front
    return population_ids[pareto_front] 



#Rank the alternatives according to their scores in the aggregation methods
def Rank(Scores):
    SortS = list(np.sort(np.array(Scores))[::-1])
    Final = []
    anc=-10000000
    for j in range(len(SortS)):
        if SortS[j] != anc:
            anc = SortS[j]
            fin=[]
            for k in range(len(Scores)):
                if Scores[k] == SortS[j]:
                    fin = fin+[k]
            Final = Final+[fin]
            
    Final2 = [0]*len(Scores)
    for i in range(len(Final)):
        for j in range(len(Final[i])):
            Final2[Final[i][j]] = i+1

    
    return Final2


#Borda aggregation method
def Borda(rankings):
    Scores = [0]*rankings.shape[0]
    
    for i in range(rankings.shape[0]):
        for j in range(rankings.shape[1]):
            for k in range(rankings.shape[0]):
                if rankings[k][j] > rankings[i][j]:
                    Scores[i] += 1
    
    return Rank(Scores)


#Condorcet aggregation method
def Condorcet(rankings):
    Scores = [0]*rankings.shape[0]
    
    for i in range(rankings.shape[0]):
        for j in range(i+1, rankings.shape[0]):
            AbatB = 0
            BbatA = 0
            for k in range(rankings.shape[1]):
                if rankings[i][k] < rankings[j][k]:
                    AbatB += 1
                if rankings[i][k] > rankings[j][k]:
                    BbatA += 1           
            if(AbatB > BbatA):
                Scores[i] = Scores[i]+1
            if(BbatA > AbatB):
                Scores[j] = Scores[j]+1
    
    return Rank(Scores)


#Copeland aggregation method
def Copeland(rankings):
    Scores = [0]*rankings.shape[0]
    
    for i in range(rankings.shape[0]):
        for j in range(i+1, rankings.shape[0]):
            AbatB = 0
            BbatA = 0
            for k in range(rankings.shape[1]):
                if rankings[i][k] < rankings[j][k]:
                    AbatB += 1
                if rankings[i][k] > rankings[j][k]:
                    BbatA += 1           
            if(AbatB > BbatA):
                Scores[i] = Scores[i]+1
                Scores[j] = Scores[j]-1
            if(BbatA > AbatB):
                Scores[j] = Scores[j]+1
                Scores[i] = Scores[i]-1
    
    return Rank(Scores)


#Majority voting
def Majority(rankings):
    Scores = [0]*rankings.shape[0]
    
    for i in range(rankings.shape[0]):
        for j in range(rankings.shape[1]):
            if rankings[i][j] == 1:
                Scores[i] += 1
    
    return Rank(Scores)


#Bucklin voting
def BucklinPlus(rankings):
    Fin = False
    depth = 1
    
    Scores = [0]*rankings.shape[0]
    
    while not Fin:
        for i in range(rankings.shape[0]):
            for j in range(rankings.shape[1]):
                if rankings[i][j] == depth:
                    Scores[i] += 1
                    if Scores[i] > rankings.shape[1]/2:
                        Fin = True
        depth += 1
    
    return Rank(Scores)    
 
    
'''
Explanation method
'''

#Complements a set of criteria
def complem(S,rankings):
    R = list(range(rankings.shape[1]))
    for s in S:
        R.remove(s)
    return list(R)

#Associates to a criterion set CP its Pareto front
def CP2Pareto(CP,rankings):
    if len(CP) == 0:
        return []
    else:
        return Pareto(rankings[:, CP])

#Associates to a Pareto front the lectically-maximal, minimal set of criteria that produce it
def Pareto2CP(pareto, B, rankings):
    S = copy.deepcopy(B)
    for i in reversed(range(rankings.shape[1])):
        if i not in S:
            X = copy.deepcopy(S)
            X.append(i)
            P = CP2Pareto(complem(X, rankings), rankings)
            if set(P)==set(pareto):
                S.append(i)
    return S
    
#Generates the next closed set of criteria
def oplusPF(A, a, rankings):
    B = [i for i in A if i < a]
    B.append(a)
    B = Pareto2CP(CP2Pareto(complem(B, rankings), rankings), B, rankings)
    return B

#Generates the next closed set of criteria in the lectic order
def NextPF(A, rankings):
    for i in reversed(range(rankings.shape[1])):
        if i not in A:
            B = oplusPF(A, i, rankings)
            if i == min(diff(B, A)):
                return B

#Computes the fixed points of the interior operator resulting from the compositions of CP2Pareto and Pareto2CP
def NextClosurePF(rankings):
    A = []
    Concepts = []
    first = True
    while len(A) != rankings.shape[1]:
        if not first:
            Concepts.append([complem(A, rankings), list(CP2Pareto(complem(A, rankings), rankings))])
        first = False
        A = NextPF(A, rankings)
    Concepts.append([complem(A, rankings), list(CP2Pareto(complem(A, rankings), rankings))])
    return Concepts


#Returns the minimal sets of criteria required to the alternative alt to appear on the Pareto front
def minCritSets(alt, rankings):
    R = []
    Concepts = np.array(NextClosurePF(rankings))
    last = []
    for i in reversed(range(Concepts.shape[0])):
        if alt in Concepts[i][1] and (last == [] or not contains(Concepts[i][0],last)):
            last = Concepts[i][0]
            R.append(Concepts[i][0])
    return R


#Returns interpretations of the reason why alternatives appear on the Pareto front according to background knowledge on the criteria
def constructInterpretation(rankings, knowlCrit, knowledge):
    PF = Pareto(rankings)
    R = []
    for alt in PF:
        MCS = minCritSets(alt, rankings)
        uni = []
        for S in MCS:
            interprets = []
            for s in S:
                interprets.append(logicalClosure(knowlCrit[s],knowledge))
            intersec = interprets[0]
            for i in range(1,len(interprets)):
                intersec = intersect(intersec,interprets[i])
            uni = union(uni,intersec)
        R.append(uni)
    return R
        
                
                
    

            
            
            
            