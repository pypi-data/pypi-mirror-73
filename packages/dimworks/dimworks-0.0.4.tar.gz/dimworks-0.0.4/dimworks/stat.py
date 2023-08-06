import pandas as pd
import numpy as np
from math import floor

def get_pp(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float)):

    std=data_1d.std()
    if USL>LSL and std>0 :
        pp = (USL - LSL) /( 6 * std)
    else:
        pp=0
        
    return round(pp,3)
    
def get_ppk(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float)):
    
    mean=data_1d.mean()
    std=data_1d.std()
    if USL>LSL and std>0 :
        ppk = min((USL-mean),(mean - LSL)) /( 3 *std)
    else:
        ppk=0
   
    return round(ppk,3)
   
def get_cp(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float),subgroupsize=5):
    rbar=get_rbar(data_1d,subgroupsize)
    d2=get_d2(subgroupsize)
    if USL>LSL and round(rbar,3)>0:
        cp=(USL-LSL)/(6*rbar/d2)
    else:
        cp=0

    return round(cp,3)

def get_cpk(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float),subgroupsize=5):
    
    mean=data_1d.mean()
    rbar=get_rbar(data_1d,subgroupsize)
    d2=get_d2(subgroupsize)

    if USL>LSL and round(rbar,3)>0:
        cpk=min((USL-mean),(mean - LSL)) /(3 * rbar/d2)
    else:
        cpk=0

    return round (cpk,3)
  

def get_xbar(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float)):
    xbar=data_1d.mean()
    
    xbar_green=0
    xbar_yellow=0
    xbar_red=0
        
    U75=(USL+LSL)/2+(USL-LSL)*0.75/2
    L75=(USL+LSL)/2-(USL-LSL)*0.75/2

    if xbar>USL or xbar<LSL:
        xbar_red=1
    elif xbar <= U75 and xbar >= L75:
        xbar_green=1
    else:
        xbar_yellow=1
    
    return xbar_green,xbar_yellow,xbar_red

def get_pc(data_1d: (pd.Series, np.array),
            USL: (int, float), LSL: (int, float)):
  
    pc_green=0
    pc_yellow=0
    pc_red=0
    pc_missing=0
    
    U75=(USL+LSL)/2+(USL-LSL)*0.75/2
    L75=(USL+LSL)/2-(USL-LSL)*0.75/2

    for d in data_1d:
        if pd.notna(d):
            if d>USL or d<LSL:
                pc_red+=1
            elif d <= U75 and d >= L75:
                pc_green+=1
            else:
                pc_yellow+=1

    pc_missing=data_1d.isna().sum()

    return pc_green,pc_yellow,pc_red,pc_missing

def get_rbar(data_1d: (pd.Series, np.array),subgroupsize=5):
    subgroupnumber=floor(data_1d.size/subgroupsize)
    r = data_1d.groupby(data_1d.index//subgroupsize).max()-data_1d.groupby(data_1d.index//subgroupsize).min()
    if subgroupnumber>0:
        rbar=r[:subgroupnumber-1].mean()
    else:
        rbar=r.mean()

    return rbar


def get_d2(subgroupsize):
    d2List=[1.128,1.693,2.059,2.326,2.534,2.704,2.847,2.970,3.078,3.173,3.259,3.336,3.407,3.472]
    if subgroupsize>15:
        subgroupsize=15
    d2=d2List[subgroupsize-2]
    return d2