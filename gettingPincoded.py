# -*- coding: utf-8 -*-
"""
Created on Sun May  2 18:23:12 2021

@author: Sumit
"""

import pandas as pd



df = pd.read_csv('IndiaPincode.csv',encoding='windows-1252')

pinCodeList = df['Pincode'].values
pinCodeList = list(set(pinCodeList))