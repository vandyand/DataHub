# =============================================================================
# This is copied and modified from the python file in the batch_file_path below
# 
# =============================================================================

import os
import calendar
import time
from datetime import datetime, timedelta
from filepaths import filepaths as fps

filepaths = fps()


    
data_hub_file_path = filepaths['DataHub']
back_file_path = filepaths['Back']
live_file_path = filepaths['Live']
batch_file_paths = [filepaths['MT-1'],filepaths['MT-2'],filepaths['MT-3']]
params_sets_file_paths = [filepaths['MT-1tester'],filepaths['MT-2tester'],
                          filepaths['MT-3tester']]


        
os.chdir(data_hub_file_path)

contents = open('hyperparameters.txt','r+').read()

content = []
for i in contents.split('\n'):
    content.append(i.split(' = '))

import sys
try:
    hyper_iterator = int(sys.argv[1])
except Exception as e:
    print(str(e))
    hyper_iterator = 0

if sum(1 for line in open('hyperparameters.txt'))==40:
    hyper_iterator = 0

hyper_lines_per_iterator = 40

# Editable parameters
##########################################################
#
#
# Meta Parameters
num_iterations = int(content[0+hyper_lines_per_iterator*hyper_iterator][1]) # Number of time_periods to go back 
back_step_size = int(content[1+hyper_lines_per_iterator*hyper_iterator][1]) #How many work days to go back per iteration
back_steps     = int(content[2+hyper_lines_per_iterator*hyper_iterator][1]) # For determining start date (2 * 5 work days (step_size) = 10 work days = 2 weeks)
fore_steps     = int(content[3+hyper_lines_per_iterator*hyper_iterator][1]) # For determining start and split date
#
start_year     = int(content[4+hyper_lines_per_iterator*hyper_iterator][1])
start_month    = int(content[5+hyper_lines_per_iterator*hyper_iterator][1])
start_day      = int(content[6+hyper_lines_per_iterator*hyper_iterator][1])
#
# EA Parameters (for EchoDiscreteModelMaker)
EA                     = content[7+hyper_lines_per_iterator*hyper_iterator][1]
symbol                 = content[8+hyper_lines_per_iterator*hyper_iterator][1]
spread                 = int(content[9+hyper_lines_per_iterator*hyper_iterator][1])
lookback_time_days     = float(content[10+hyper_lines_per_iterator*hyper_iterator][1]) #For opening and closing trades parameters
holding_time_days      = float(content[11+hyper_lines_per_iterator*hyper_iterator][1])
timeframe              = int(content[12+hyper_lines_per_iterator*hyper_iterator][1]) #minutes
Chart_Timeframe        = content[13+hyper_lines_per_iterator*hyper_iterator][1]
optimization_score_num = content[14+hyper_lines_per_iterator*hyper_iterator][1]
file_name_prefix_vers  = int(content[15+hyper_lines_per_iterator*hyper_iterator][1])
threshold              = int(content[16+hyper_lines_per_iterator*hyper_iterator][1]) # This is the latest previously run file prefix. 
#                                   # Use this if you want to continue (expand on) a previously backtested set of parameters...
#                                   # in which case threshold is the number of the last file in the set and
#                                   # num_iterations plus fine_name_prefix_vers is how high it will go.
data_set_num           = int(content[17+hyper_lines_per_iterator*hyper_iterator][1])# For which folder to move results into in data hub file
num_backtests_per_set  = int(content[18+hyper_lines_per_iterator*hyper_iterator][1])
#
#
num_iterations += threshold
##########################################################



# Setting up computer file parameters
date_list = [datetime.strftime(datetime(start_year,start_month,start_day) - timedelta(days=x),'%Y.%m.%d') for x in range(10000) if (datetime(start_year,start_month,start_day)-timedelta(days=x)).weekday() not in [0,6] ]
start_dates = [date_list[(x+back_steps+fore_steps)*back_step_size] for x in range(num_iterations)]
split_dates = [date_list[(x+fore_steps)*back_step_size] for x in range(num_iterations)]
end_dates = [date_list[x*back_step_size] for x in range(num_iterations)]
split_datetimes = [calendar.timegm(time.strptime(x,'%Y.%m.%d')) for x in split_dates]
file_nameishes = ['{}'.format(x+1+file_name_prefix_vers) for x in range(num_iterations)]
param_file_names = ['iter{}.txt'.format(x+1) for x in range(num_iterations)]
set_file_names = ['iter{}.set'.format(x+1) for x in range(num_iterations)]


# EA computer parameters
bars_in_lookback = int(lookback_time_days*24*60/timeframe) # days * hours/day * bars/hour
bars_in_holding = int(holding_time_days*24*60/timeframe)

Long_Back_1_Start = int(content[19+hyper_lines_per_iterator*hyper_iterator][1])
Long_Back_1_Step = int(content[20+hyper_lines_per_iterator*hyper_iterator][1])
Long_Back_1_End = bars_in_lookback
Long_Back_2_Start = int(content[21+hyper_lines_per_iterator*hyper_iterator][1])
Long_Back_2_Step = int(content[22+hyper_lines_per_iterator*hyper_iterator][1])
Long_Back_2_End = bars_in_lookback
Short_Back_1_Start = int(content[23+hyper_lines_per_iterator*hyper_iterator][1])
Short_Back_1_Step = int(content[24+hyper_lines_per_iterator*hyper_iterator][1])
Short_Back_1_End = bars_in_lookback
Short_Back_2_Start = int(content[25+hyper_lines_per_iterator*hyper_iterator][1])
Short_Back_2_Step = int(content[26+hyper_lines_per_iterator*hyper_iterator][1])
Short_Back_2_End = bars_in_lookback
Open_Bars_Start = int(content[27+hyper_lines_per_iterator*hyper_iterator][1])
Open_Bars_Step = int(content[28+hyper_lines_per_iterator*hyper_iterator][1])
Open_Bars_End = bars_in_holding
Lots_Value = float(content[29+hyper_lines_per_iterator*hyper_iterator][1])

get_random_results = int(content[30+hyper_lines_per_iterator*hyper_iterator][1])
only_positive_results = int(content[31+hyper_lines_per_iterator*hyper_iterator][1])
back_or_live = int(content[32+hyper_lines_per_iterator*hyper_iterator][1])

if back_or_live==0:
    set_file_path = back_file_path
elif back_or_live==1:
    set_file_path = live_file_path

for j in range(3):

    for i in range(j%3,num_iterations,3):
        
        if(i>threshold-1):
        
            # Set file creation
            os.chdir(params_sets_file_paths[j])
        
            split_datetime = split_datetimes[i]
            file_nameish = file_nameishes[i]
            
            
            set_file_content = '''Long_Back_1=0
Long_Back_1,F=1
Long_Back_1,1={}
Long_Back_1,2={}
Long_Back_1,3={}
Long_Back_2=0
Long_Back_2,F=1
Long_Back_2,1={}
Long_Back_2,2={}
Long_Back_2,3={}
Short_Back_1=0
Short_Back_1,F=1
Short_Back_1,1={}
Short_Back_1,2={}
Short_Back_1,3={}
Short_Back_2=0
Short_Back_2,F=1
Short_Back_2,1={}
Short_Back_2,2={}
Short_Back_2,3={}
Open_Bars=0
Open_Bars,F=1
Open_Bars,1={}
Open_Bars,2={}
Open_Bars,3={}
prof_factr_thresh=1.00000000
prof_factr_thresh,F=0
prof_factr_thresh,1=0.00000000
prof_factr_thresh,2=0.00000000
prof_factr_thresh,3=0.00000000
recov_factr_thresh=0.00000000
recov_factr_thresh,F=0
recov_factr_thresh,1=0.00000000
recov_factr_thresh,2=0.00000000
recov_factr_thresh,3=0.00000000
sharpe_thresh=0.00000000
sharpe_thresh,F=0
sharpe_thresh,1=0.00000000
sharpe_thresh,2=0.00000000
sharpe_thresh,3=0.00000000
score_thresh=0.00000000
score_thresh,F=0
score_thresh,1=0.00000000
score_thresh,2=0.00000000
score_thresh,3=0.00000000
num_trades_thresh=1
num_trades_thresh,F=0
num_trades_thresh,1=1
num_trades_thresh,2=0
num_trades_thresh,3=0
split_datetime={}
split_datetime,F=0
split_datetime,1=0
split_datetime,2=0
split_datetime,3=0
write_to_file=1
write_to_file,F=0
write_to_file,1=0
write_to_file,2=1
write_to_file,3=1
file_name_prefix={}
file_name_prefix,F=0
file_name_prefix,1=0
file_name_prefix,2=0
file_name_prefix,3=0
score_type={}
score_type,F=0
score_type,1=0
score_type,2=0
score_type,3=0
Lots={}
Lots,F=0
Lots,1=0.00000000
Lots,2=0.00000000
Lots,3=0.00000000
get_random_results={}
get_random_results,F=0
get_random_results,1=0
get_random_results,2=1
get_random_results,3=1
only_positive_results={}
only_positive_results,F=0
only_positive_results,1=0
only_positive_results,2=1
only_positive_results,3=1
'''.format(Long_Back_1_Start,Long_Back_1_Step,Long_Back_1_End,
Long_Back_2_Start,Long_Back_2_Step,Long_Back_2_End,Short_Back_1_Start,
Short_Back_1_Step,Short_Back_1_End,Short_Back_2_Start,Short_Back_2_Step,
Short_Back_2_End,Open_Bars_Start,Open_Bars_Step,Open_Bars_End,split_datetime,
file_nameish,optimization_score_num,Lots_Value,get_random_results,
only_positive_results)
            
            set_file_name = set_file_names[i]
            set_file = open(set_file_name,'a')
            set_file.write(set_file_content)
            set_file.close()
            
            
            # Param file creation
            start_date = start_dates[i]
            end_date = end_dates[i]
            
            param_file_content = '''; start strategy tester 
TestExpert={} 
TestExpertParameters={} 
TestSymbol={} 
TestPeriod={} 
TestModel=2 
TestSpread={} 
TestOptimization=true 
TestDateEnable=true 
TestFromDate={} 
TestToDate={} 
TestShutdownTerminal=true
'''.format(EA,set_file_name,symbol,Chart_Timeframe,spread,start_date,end_date)
            
            param_file_name = param_file_names[i]
            param_file = open(param_file_name,'a')
            param_file.write(param_file_content)
            param_file.close()
            
            
            # Set# folder and summary params file creation
        
            
            
            if not os.path.exists("{}\\Set{}".format(set_file_path,data_set_num)):
                os.makedirs("{}\\Set{}".format(set_file_path,data_set_num))
                os.chdir("{}\\Set{}".format(set_file_path,data_set_num))
                a = open('parameters.txt','w')
                a.write('''num_iterations = {}
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
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
holder = 0
'''.format(num_iterations,back_step_size,back_steps,fore_steps,
start_year,start_month,start_day,EA,symbol,spread,lookback_time_days,
holding_time_days,timeframe,Chart_Timeframe,optimization_score_num,
file_name_prefix_vers,threshold,data_set_num,num_backtests_per_set,
Long_Back_1_Start,Long_Back_1_Step,Long_Back_2_Start,Long_Back_2_Step,
Short_Back_1_Start,Short_Back_1_Step,Short_Back_2_Start,Short_Back_2_Step,
Open_Bars_Start,Open_Bars_Step,Lots_Value,get_random_results))
                a.close()
            
            
            
            #Batch files creation
            
            os.chdir(batch_file_paths[j])
            
            batch_file_name = 'batch_backtests.bat'
            batch_file = open(batch_file_name, 'a')
            
            for i in range(num_backtests_per_set):
                batch_file_content = '''start /wait /min "" "{}"\\terminal.exe /portable "{}"\{}\n
'''.format(batch_file_paths[j],params_sets_file_paths[j],param_file_name)
                batch_file.write(batch_file_content)
            
            move_content = '''move "{}\\files\\{}_{}.csv" "{}\\Set{}"\n
'''.format(params_sets_file_paths[j],file_nameish,symbol,set_file_path,data_set_num)
            batch_file.write(move_content)
            
            batch_file.close()

#for j in range(3):
#    os.chdir(batch_file_paths[j])
#    batch_file = open('batch_backtests.bat','a')
#    batch_file.write('\n\n\nEXIT /B 0 \n\n\n')
#    batch_file.close()

os.chdir(data_hub_file_path)

master_batch_file = open('master_batch_file.bat','a')

#for j in range(3):#/B CMD /C CALL
#    master_batch_file.write('''start "{}" "{}\{}"\n\n\n'''.format(j,batch_file_paths[j],batch_file_name))
#for j in range(3):   
#    master_batch_file.write('\n\n\nEXIT\n\n\n')
#master_batch_file.write('exit\n\n')


master_batch_file.write('mparallel.exe --count=3 --shell {}\{} : {}\{} : {}\{}\nexit'.format(
        batch_file_paths[0],batch_file_name,
        batch_file_paths[1],batch_file_name,
        batch_file_paths[2],batch_file_name))


master_batch_file.close()
    
    
    
