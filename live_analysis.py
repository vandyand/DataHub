

import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import scipy.stats as st
from filepaths import filepaths as fps

filepaths = fps()

data_hub_file_path = filepaths['DataHub']
back_file_path = filepaths['Back']
live_file_path = filepaths['Live']


print("Running live_analysis.py...")

os.chdir(data_hub_file_path)

try:
    hyper_iterator = int(sys.argv[1])
except Exception:
    hyper_iterator = 0

if sum(1 for line in open('hyperparameters.txt'))==40:
    hyper_iterator = 0

hyper_lines_per_iterator = 40

contents = open('hyperparameters.txt','r+').read()
content = []
for i in contents.split('\n'):
    content.append(i.split(' = '))

symbol       = content[8+hyper_lines_per_iterator*hyper_iterator][1]
spread       = int(content[9+hyper_lines_per_iterator*hyper_iterator][1])
data_set_num = int(content[17+hyper_lines_per_iterator*hyper_iterator][1])

#data_set_num = 1002

data_file_path = '{}\\Set{}'.format(live_file_path,data_set_num)

os.chdir(data_file_path)
num_files = len([x for x in os.listdir() if '.csv' in x])


cols = ['btrades','ftrades',
        'Long_Back_1','Long_Back_2','Short_Back_1','Short_Back_2','Open_Bars']


#mean_returns = []
#file_count = 0
def import_data(filepath):
    data = pd.read_csv(filepath,header=None)
    data.columns = cols
    data = data.drop_duplicates(['btrades','ftrades']).reset_index(drop=True)
    data.fillna('0.0',inplace=True)
    data = data.reset_index(drop=True)
#    mean_returns.append(data['fprofit'].mean())
#    global file_count
#    file_count += 1
#    print(file_count)
    return(data)

print('Importing data...')
final_data = [ import_data('{}\Set{}\{}'.format(live_file_path,data_set_num,f)) for f in os.listdir() if '.csv' in f]


#print("\n",np.mean(mean_returns),np.std(mean_returns))

count = 0
# Get back stats
for data in final_data:
    print(str(count+1)+' out of '+str(len(final_data))+' calculating...')
    lenn = data.shape[0]
    print('...calculating bsplits...')
    bsplits  = [ data['btrades'][x].split() for x in range(lenn) ]
    print('...calculating btrades...')
    data['btrades'] = [ [float(bsplits[x][y]) for y in range(len(bsplits[x]))] for x in range(len(bsplits)) ]
    data['bpos_trades'] = [ [data['btrades'][x][y] for y in range(len(data['btrades'][x])) if data['btrades'][x][y]>0] for x in range(lenn) ]
    data['bneg_trades'] = [ [data['btrades'][x][y] for y in range(len(data['btrades'][x])) if data['btrades'][x][y]<=0] for x in range(lenn) ]
    data['bnum_trades'] = [ len(data['btrades'][x]) for x in range(lenn) ]
    print('...calculating gross profit...')
    data['bgross_profit'] = [ sum(data['bpos_trades'][x]) for x in range(lenn) ]
    data['bgross_loss'] = [ sum(data['bneg_trades'][x]) for x in range(lenn) ]
    data['bprofit'] = data['bgross_profit'] + data['bgross_loss']
    print('...calculating profit factor...')
    data['bprofit_factor'] =[ data['bgross_profit'][x] / data['bgross_loss'][x] * -1 if data['bgross_loss'][x]!=0 else data['bnum_trades'][x] for x in range(lenn) ]
    data['bexpected_payoff'] = data['bprofit'] / data['bnum_trades']
    print('...calculating standard deviation...')
    data['bstd'] = [ np.std(data['btrades'][x]) if np.std(data['btrades'][x])>0.00001 else 0 for x in range(lenn) ]
    data['bneg_std'] = [ np.std(data['bneg_trades'][x]) if bool(data['bneg_trades'][x]) and np.std(data['bneg_trades'][x])>0.00001 else 0 for x in range(lenn) ]
    print('...calculating sharpe and sortino...')
    data['bsharpe'] = [ data['bexpected_payoff'][x] / data['bstd'][x] if data['bstd'][x]!=0 else data['bnum_trades'][x] if data['bprofit'][x]>0 else data['bnum_trades'][x] * -1 for x in range(lenn) ]
    data['bsortino'] = [ data['bexpected_payoff'][x] / data['bneg_std'][x] if data['bneg_std'][x]!=0 else data['bnum_trades'][x] if data['bprofit'][x]>0 else data['bnum_trades'][x] * -1 for x in range(lenn) ]
    
    
#    fsplits  = [ data['ftrades'][x].split() for x in range(lenn) ]
#    data['ftrades'] = [ [float(fsplits[x][y]) for y in range(len(fsplits[x]))] for x in range(len(fsplits)) ]
    
    print(str(count+1)+' out of '+str(len(final_data))+' done.')
    count += 1
    

# Score engineering
properties = np.array(['bprofit','bprofit_factor','bexpected_payoff','bnum_trades',
              'bsharpe','bsortino','bstd'])
num_combinations = 2**len(properties) - 1
for i in range(1,num_combinations):
    for dataa in final_data:
        if i%int(num_combinations/20)==0:
            print('{}%'.format(round(i/num_combinations*100,0)))
        lookups = properties[[ bool(int(x)) for x in bin(i)[2:].zfill(len(properties)) ]]
        product = 1
        for j in lookups:
            product *= data[j]
        dataa['bscore{}'.format(i)] = product

os.chdir(back_file_path)
final_results_filename = [ i for i in os.listdir() if '.txt' in i ][-1]
with open(final_results_filename,'r') as final_results_file:
    sett, item, score = [ int(i) for i in final_results_file.read().split('\n')[1].split(',') ]


final_ea_params = final_data[0].sort_values('bscore{}'.format(score),ascending=False).iloc[item-1,2:7]

print(final_ea_params)

os.chdir(live_file_path)
open('final_ea_params-Set{}.txt'.format(data_set_num),'w').close()
with open('final_ea_params-Set{}.txt'.format(data_set_num),'a') as f:
    f.write(str([ i for i in final_ea_params]))











