# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 01:13:19 2018

@author: dell
"""

import os
from filepaths import filepaths as fps

os.chdir(r'C:\Users\dell\Desktop\PythonAlgoFolder\DataHub')
filepaths = fps()

# Setup what instance of MT4 to run in...
MT4_instance_num = 1
if os.environ['COMPUTERNAME'] != 'DELL-PC':
    MT4_instance_num = 7

# Setup file paths
txt_filepath = filepaths['MT-{}'.format(MT4_instance_num)]
set_filepath = filepaths['MT-{}Presets'.format(MT4_instance_num)]
tpl_filepath = filepaths['MT-{}templates'.format(MT4_instance_num)]
bat_filepath = txt_filepath



# Template generator
# Make up ea parameter values for now. Need to update analysis scripts to
# output the top five (or whatever number) best algorithms to final_results.txt
num_EAs = 5
long_back_1 = []
long_back_2 = []
short_back_1 = []
short_back_2 = []
tpl_filenames = []

# Generating values...
for i in range(num_EAs):
    long_back_1.append(list(range(20))[i*4+0])
    long_back_2.append(list(range(20))[i*4+1])
    short_back_1.append(list(range(20))[i*4+2])
    short_back_2.append(list(range(20))[i*4+3])
    tpl_filenames.append(tpl_filepath+'\\tpl'+str(i+1)+'.tpl')

Lots = 0.01


# Text file setup
txt_filename = txt_filepath+'\\script_setup.txt'
symbol = 'EURUSD'
period = 'D1'

# Set file setup
set_filename = 'script_setup.set'
timeframe = 1440 # This needs to match the text file period above.


os.chdir(tpl_filepath)

for i in range(num_EAs):
    with open(tpl_filenames[i],'w') as tpl_file:
        tpl_contents = '''<chart>
<expert>
name=DiscreteModelMaker\IndiaDiscreteModelMaker
flags=343
window_num=0
<inputs>
Long_Back_1={}
Long_Back_2={}
Short_Back_1={}
Short_Back_2={}
Open_Bars=0
prof_factr_thresh=0.0
recov_factr_thresh=0.0
sharpe_thresh=0.0
score_thresh=0.0
num_trades_thresh=1
split_datetime=0
write_to_file=false
file_name_prefix=0
score_type=0
Lots={}
get_random_results=false
only_positive_results=false
</inputs>
</expert>
</chart>
'''.format(long_back_1[i],long_back_2[i],short_back_1[i],short_back_2[i],Lots)
        tpl_file.write(tpl_contents)
    
# Now make the text file...
os.chdir(txt_filepath)
with open(txt_filename,'w') as txt_file:
    txt_contents = '''; open chart and run expert and/or script 
Symbol={} 
Period={}
Script=LoadEAs
ScriptParameters={}'''.format(symbol,period,set_filename)
    txt_file.write(txt_contents)

# Now make the set file...
os.chdir(set_filepath)
with open(set_filename,'w') as set_file:
    set_contents = '''num_EAs={}
symbol={}
timeframe={}
'''.format(num_EAs,symbol,timeframe)
    set_file.write(set_contents)



