# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 20:51:21 2018

@author: dell
"""

import os



def filepaths():
    os.chdir('C:\\users\\dell\\desktop\\pythonalgofolder\\datahub')
    with open('filepaths.txt','r') as file:
        filepaths = file.read().split('\n')
        filepaths = {t[0]:t[1] for t in [ i.split('=') for i in filepaths ]}
        filepaths['DataHub'] = filepaths['DataHub1'] if os.environ['COMPUTERNAME']=='DELL-PC' else filepaths['DataHub2']
        filepaths.pop('DataHub1',None)
        filepaths.pop('DataHub2',None)
        filepaths['Back'] = filepaths['DataHub']+'\\Back'
        filepaths['Live'] = filepaths['DataHub']+'\\Live'
        for i in range(2,7):
            filepaths['MT-{}'.format(i)] = filepaths['MT-1'][:-1]+str(i)
        for i in range(1,7):
            filepaths['MT-{}tester'.format(i)] = filepaths['MT-{}'.format(i)]+'\\tester'
            filepaths['MT-{}templates'.format(i)] = filepaths['MT-{}'.format(i)]+'\\templates'
            filepaths['MT-{}Experts'.format(i)] = filepaths['MT-{}'.format(i)]+'\\MQL4\\Experts'
            filepaths['MT-{}Presets'.format(i)] = filepaths['MT-{}'.format(i)]+'\\MQL4\\Presets'
            
    return filepaths
    
    
    
    
    