# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 20:51:21 2018

@author: dell
"""

import os

def filepaths():
    with open('filepaths.txt','r') as file:
        filepaths = file.read().split('\n')
        filepaths = {t[0]:t[1] for t in [ i.split('=') for i in filepaths ]}
        filepaths['DataHub'] = filepaths['DataHub1'] if os.environ['COMPUTERNAME']=='DELL-PC' else filepaths['DataHub2']
        filepaths.pop('DataHub1',None)
        filepaths.pop('DataHub2',None)
        filepaths['Back'] = filepaths['DataHub']+'\\Back'
        filepaths['Live'] = filepaths['DataHub']+'\\Live'
    return filepaths
    
    
    
    
    