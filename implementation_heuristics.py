import numpy as np 
import pandas as pd
from algorithms import Algorithms as al
import os

#SAMPLE 1
demand1 = np.array([100,240,120,70,50,40,30])
c1 = 100
h1 = 0.4

#SAMPLE 2 (Taken from Principles Of Inventory And Materials Management)
demand2 = np.array([75,0,33,28,0,10]) 
c2 = 100
h2 = 1 

sample1 = [demand1, c1, h1]
sample2 = [demand2, c2, h2]


samples = [[sample1,"SAMPLE1"], [sample2,"SAMPLE2"]]

for i in samples:
    
    print(f"\n\n{i[1]}")
    print(f"------------------------------------\n\n")
    
    print("Part Period Balancing")
    print("--------------------------")
    ppb = al.PartPeriodBalancing(*i[0])
    ppb.print_result()
    
    
    print("\nSilver Meal Method")
    print("--------------------------")
    sm = al.SilverMeal(*i[0])
    sm.print_result()
    
    
    print("\nLeast Unit Cost Method")
    print("--------------------------")
    luc = al.LeastUnitCost(*i[0])
    luc.print_result()