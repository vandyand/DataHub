# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 22:29:55 2018

@author: dell
"""


from datetime import datetime
import time
import psutil
import os
import subprocess

data_hub_file_path = 'C:\\Users\\Dell\\Desktop\\PythonAlgoFolder\\DataHub'
live_file_path = data_hub_file_path + '\\Live'

# Rolling_runner update frequency (seconds) - This is the period for dictating
# when the body of the code (below) runs.
reset_period = 60 # Reset every ____ seconds.

# setup .txt file parameters
txt_file_path = "C:/Program Files (x86)/OANDA - MetaTrader" # Same as batch_file_path from big_master_backtests_generator.py
filename_txt = 'setup_live_ea.txt'
symbol = 'AUDUSD'
period = 'M1' # This is the ea chart period, not the rolling_runner update period
expert = 'DiscreteModelMaker/IndiaDiscreteModelMaker'

# setup .set file parameters
set_file_path = "C:/Program Files (x86)/OANDA - MetaTrader/MQL4/Presets"
filename_set = 'setup_live_ea.set'
long_back_1 = 0
long_back_2 = 0
short_back_1 = 0
short_back_2 = 0
lots = 0.01

# .bat file parameters
bat_file_path = txt_file_path
filename_bat = 'setup_live_ea.bat'


os.chdir(live_file_path)

count = 0
start = False

while True:
    # Start_cond is for when to start it. The whole system should update itself
    # (start).
    start_cond = datetime.weekday(datetime.now()) in range(5)      \
                 and int(datetime.timestamp(datetime.now())) % reset_period == 0
    print(int(datetime.timestamp(datetime.now())) % reset_period)
    time.sleep(0.99)

    
    # Start master_hyper_setup.py which sets everything up and runs the backtest(s)
    # if current time is a weekday at 5:00PM EST (0=Monday etc... hour 17 = 5:00pm)
    # Make sure master_hyper_setup has the parameters you want before starting
    # this whole thing - really it should get parameters...
    if start_cond: 
        # Kill all currently running metatrader (called terminal.exe)
        for process in (p for p in psutil.process_iter() if 'terminal.exe' in p.name()):
            process.kill()
        
        print('start is true')
        os.chdir(data_hub_file_path)
        subprocess.call("master_hyper_setup.py", shell=True)
        
    # when the above is done read the output file to get the right parameters
    # for the live test strategy. The output file is named
    # final_ea_params-Set####.txt in the "Live" directory.
#    os.chdir(live_file_path)
#    if start and file_condition:
        os.chdir(live_file_path)    
        final_ea_params_filename = [ i for i in os.listdir() if '.txt' in i if str(datetime.now().year)+str(datetime.now().month).zfill(2)+str(datetime.now().day).zfill(2)+str(datetime.now().hour).zfill(2) in i ][-1]
        with open(live_file_path+'\\'+final_ea_params_filename,'r') as params_file:
            ea_params = params_file.read()
            ea_params = [ int(i) for i in ea_params.replace('[','').replace(']','').replace(' ','').split(',') ]
            long_back_1 = ea_params[0]
            long_back_2 = ea_params[1]
            short_back_1 = ea_params[2]
            short_back_2 = ea_params[3]
    
    # Next launch a mt4 terminal with these parameters.
    # Open trades will be handled by the strategy 
    # (test this to make sure it works). It should work except when there's
    # an open sell position and now it's switching to long... TODO item.
    
    # To open an MT4 terminal with a running live ea you need to create or 
    # update the chart parameters in a .txt file in main metatrader directory.
    # This file points to a .set file in the /mql4/presets directory. The .set 
    # file has all the ea parameters in it.
    
    
    # Create .txt, .set and batch files:
    
    # Create .txt file
        print('creating .txt file')
        os.chdir(txt_file_path)
        txt_file = open(filename_txt,'w')
        txt_file_contents = '''Symbol={} 
Period={}
Expert={}
ExpertParameters={}'''.format(symbol,period,expert,filename_set)
        txt_file.write(txt_file_contents)
        txt_file.close()
    
    # Create .set file
        print('creating .set file')
        os.chdir(set_file_path)
        set_file = open(filename_set,'w')
        set_file_contents = '''Long_Back_1={}
Long_Back_2={}
Short_Back_1={}
Short_Back_2={}
Open_Bars=0
prof_factr_thresh=1.00000000
recov_factr_thresh=0.00000000
sharpe_thresh=0.00000000
score_thresh=0.00000000
num_trades_thresh=1
split_datetime=0
write_to_file=0
file_name_prefix=1
score_type=0
Lots={}
get_random_results=1
only_positive_results=0'''.format(long_back_1,long_back_2,short_back_1,
short_back_2,lots)
        set_file.write(set_file_contents)
        set_file.close()
    
    # Create batch file
        print('creating .bat file')
        os.chdir(bat_file_path)
        bat_file = open(filename_bat,'w')
        bat_file_contents = '''terminal.exe /portable {}'''.format(filename_txt)
        bat_file.write(bat_file_contents)
        bat_file.close()
        
    # Run batch file
        print('starting .bat file')
        os.startfile(filename_bat)
    
    # Finally, reset file_condition to [] empty set for oneshot logic above
    file_condition = []

