# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 20:51:21 2018

@author: dell
"""

def filepaths():
    file = open('filepaths.txt','r')
    filepaths = file.read().split('\n')
    filepaths = {t[0]:t[1] for t in [ i.split('=') for i in filepaths ]}
    file.close()
    return filepaths
    
    
    
    
    