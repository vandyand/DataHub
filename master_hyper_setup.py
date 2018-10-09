
from datetime import datetime
from filepaths import filepaths as fps

filepaths = fps()

# Set this value to True if you're going to run live with rolling_runner.py
# Rolling_runner.py is what's used for live testing this whole system.
rolling_runner = False

# Hyperparameters:
num_iterations = 15 # Number of time_periods to go back
back_step_sizes = [1]#[20,10,5,1] #How many work days to go back per iteration (20 workdays = 4 weeks, etc...)
back_stepss = [3]#[3,4,5]# For determining start date (For example 2 back_steps * 5 work days (back_step_size) = 10 work days = 2 weeks)
fore_stepss = [1]#[1,2]# For determining start and split date

back_or_live = 0 #0 = back, 1 = live #If it's live it can't do the fore part...
                 #because that's literally into the future.
if rolling_runner:
    back_or_live = 1 # It has to be live when using rolling_runner.py

if back_or_live==1:
    num_iterations = 1


# Set this to true if you want custom start times (Setting it to false allows 
# the roller_runner.py to always be up to date)
start_at_current_time = True
if start_at_current_time or rolling_runner: 
    start_year = datetime.now().year
    start_month = datetime.now().month
    start_day = datetime.now().day
else: #Modify these values for custom start datetime (really end...)
    start_year = 2018
    start_month = 8
    start_day = 31


    
data_set_num = int(str(datetime.now().year)+str(datetime.now().month).zfill(2)+str(datetime.now().day).zfill(2)+str(datetime.now().hour).zfill(2)+str(datetime.now().minute).zfill(2)+str(datetime.now().second).zfill(2))

EA = "DiscreteModelMaker\IndiaDiscreteModelMaker"
symbols = ['AUDUSD']
spread = 15


# EA Parameters
lookback_time_dayss = [5]#[50,10,5,2]#For opening and closing trades parameters
holding_time_dayss = [1] # This has no effect for hotel and india as they're 
                         # not looking at Open_Bars for a closing condition.
Chart_Timeframes = ['M15']
timeframe_lookup = {'M1':1,'M5':5,'M15':15,'M30':30,'H1':60,'H4':240,
                    'D1':1440,'W1':7200}#This is just a reference. Don't modify
                                        #this.

optimization_score_num = 0 #I believe this is superfluous when
                           #get_random_results is true
file_name_prefix_vers = 0 # I don't remember what this does... :) Something with file_nameish which goes all the way back to mql4 stuff... whatever.
threshold = 0 # This is the latest previously run file prefix. 
              # Use this if you want to continue (expand on) a previously backtested set of parameters...
              # in which case threshold is the number of the last file in the set and
              # num_iterations plus fine_name_prefix_vers is how high it will go.

num_backtests_per_set = 1 #This is how many times metatrader 4 is called per
                          #parameter set

# These are the parameters for the optimizations in MT4
Long_Back_1_Start = 1
Long_Back_1_Step = 1
Long_Back_2_Start = 1
Long_Back_2_Step = 1
Short_Back_1_Start = 1
Short_Back_1_Step = 1
Short_Back_2_Start = 1
Short_Back_2_Step = 1
Open_Bars_Start = 2
Open_Bars_Step = 1
if EA == "DiscreteModelMaker\IndiaDiscreteModelMaker" or EA == "DiscreteModelMaker\HotelDiscreteModelMaker":
    Open_Bars_Step = 0 # Because india and hotel don't use open_bars for open positions hold time
                       # (not that it should matter because it should be random anyways...)
Lots_Value = 0.01
get_random_results = 1
only_positive_results = 0


# File parameters
hyper_lines_per_iterator = 40

data_hub_file_path = filepaths['DataHub']

import os
try:
    os.remove('{}\\mamamamaster.bat'.format(data_hub_file_path))
except Exception:
    pass
try:
    os.remove('{}\\hyperparameters.txt'.format(data_hub_file_path))
except Exception:
    pass

mamamamaster_file = open('mamamamaster.bat', 'a')
mamamamaster_file.write('''python ini_genetic_param.py 1
python copy_eas.py

''')


hyperparameters_file = open('hyperparameters.txt','a')


# This part writes the hyperparameters.txt file which has a section for each
# unique parameter set. big_master_backtests_generator.py gets it's parameter
# values from this file. It knows where to look via a system argument in the 
# batch file.
for symbol in symbols:
    for holding_time_days in holding_time_dayss:
        for lookback_time_days in lookback_time_dayss:
            for fore_steps in fore_stepss:
                for back_steps in back_stepss:
                    for back_step_size in back_step_sizes:
                        for Chart_Timeframe in Chart_Timeframes:
                            timeframe = timeframe_lookup[Chart_Timeframe]
                            hyperparameters_file.write('''num_iterations = {}
back_step_size = {}
back_steps = {}
fore_steps = {}
start_year = {}
start_month = {}
start_day = {}
EA = {}
symbol = {}
spread = {}
lookback_time_days = {}
holding_time_days = {}
timeframe = {}
Chart_Timeframe = {}
optimization_score_num = {}
file_name_prefix_vers = {}
threshold = {}
data_set_num = {}
num_backtests_per_set = {}
Long_Back_1_Start = {}
Long_Back_1_Step = {}
Long_Back_2_Start = {}
Long_Back_2_Step = {}
Short_Back_1_Start = {}
Short_Back_1_Step = {}
Short_Back_2_Start = {}
Short_Back_2_Step = {}
Open_Bars_Start = {}
Open_Bars_Step = {}
Lots_Value = {}
get_random_results = {}
only_positive_results = {}
back_or_live = {}
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
'''.format(
num_iterations,
back_step_size,
back_steps,
fore_steps,
start_year,
start_month,
start_day,
EA,
symbol,
spread,
lookback_time_days,
holding_time_days,
timeframe,
Chart_Timeframe,
optimization_score_num,
file_name_prefix_vers,
threshold,
data_set_num,
num_backtests_per_set,
Long_Back_1_Start,
Long_Back_1_Step,
Long_Back_2_Start,
Long_Back_2_Step,
Short_Back_1_Start,
Short_Back_1_Step,
Short_Back_2_Start,
Short_Back_2_Step,
Open_Bars_Start,
Open_Bars_Step,
Lots_Value,
get_random_results,
only_positive_results,
back_or_live))

                            mamamamaster_file.write('''python delete_files.py
python big_master_backtests_generator.py {}
start /wait "" "master_batch_file.bat"

'''.format(data_set_num))

                            if back_or_live==0:
                                mamamamaster_file.write('''python golf_analysis.py {}
'''.format(data_set_num))

if back_or_live==0:
    mamamamaster_file.write('python final_analysis.py')
elif back_or_live==1:
    mamamamaster_file.write('python live_analysis.py')

mamamamaster_file.close()
hyperparameters_file.close()


# Run mamamamaster.bat file

os.system('{}\\mamamamaster.bat'.format(data_hub_file_path))

