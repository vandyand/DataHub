# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 22:29:55 2018

@author: dell
"""


from datetime import datetime
import os

data_hub_file_path = 'C:\\Users\\Dell\\Desktop\\PythonAlgoFolder\\DataHub'

while True:
    
    if datetime.weekday(datetime.now()) in range(5) and datetime.now().hour == 17: # Check if current time is a weekday at 5:00PM EST (0=Monday etc... hour 17 = 5:00pm)
        os.system('{}\\master_hyper_setup.py'.format(data_hub_file_path))

        # when this is done read the output file to get the right parameters
        # for the live test strategy and launch a mt4 terminal with these 
        # parameters. Also, kill the current mt4 terminal. Open trades will
        # be handled by the strategy (hopefully... at least that's the idea :))



