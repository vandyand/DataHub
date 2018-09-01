

import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import scipy.stats as st

data_hub_file_path = 'C:\\Users\\Dell\\Desktop\\PythonAlgoFolder\\DataHub'
back_file_path = data_hub_file_path+'\\Back'
live_file_path = data_hub_file_path+'\\Live'
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

#data_set_num = 2

data_file_path = '{}\\Set{}'.format(back_file_path,data_set_num)

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


datas = [import_data('{}\Set{}\{}'.format(back_file_path,data_set_num,f)) for f in os.listdir() if '.csv' in f]

#print("\n",np.mean(mean_returns),np.std(mean_returns))

count = 0
# Get back stats
print('Calculating back stats...')
for data in datas:
    print(str(count+1)+' out of '+str(len(datas))+' calculating...')
    lenn = data.shape[0]
    bsplits  = [ data['btrades'][x].split() for x in range(lenn) ]
    data['btrades'] = [ [float(bsplits[x][y]) for y in range(len(bsplits[x]))] for x in range(len(bsplits)) ]
    data['bpos_trades'] = [ [data['btrades'][x][y] for y in range(len(data['btrades'][x])) if data['btrades'][x][y]>0] for x in range(lenn) ]
    data['bneg_trades'] = [ [data['btrades'][x][y] for y in range(len(data['btrades'][x])) if data['btrades'][x][y]<=0] for x in range(lenn) ]
    data['bnum_trades'] = [ len(data['btrades'][x]) for x in range(lenn) ]
    data['bgross_profit'] = [ sum(data['bpos_trades'][x]) for x in range(lenn) ]
    data['bgross_loss'] = [ sum(data['bneg_trades'][x]) for x in range(lenn) ]
    data['bprofit'] = data['bgross_profit'] + data['bgross_loss']
    data['bprofit_factor'] =[ data['bgross_profit'][x] / data['bgross_loss'][x] * -1 if data['bgross_loss'][x]!=0 else data['bnum_trades'][x] for x in range(lenn) ]
    data['bexpected_payoff'] = data['bprofit'] / data['bnum_trades']
    data['bstd'] = [ np.std(data['btrades'][x]) if np.std(data['btrades'][x])>0.00001 else 0 for x in range(lenn) ]
    data['bneg_std'] = [ np.std(data['bneg_trades'][x]) if bool(data['bneg_trades'][x]) and np.std(data['bneg_trades'][x])>0.00001 else 0 for x in range(lenn) ]
    data['bsharpe'] = [ data['bexpected_payoff'][x] / data['bstd'][x] if data['bstd'][x]!=0 else data['bnum_trades'][x] if data['bprofit'][x]>0 else data['bnum_trades'][x] * -1 for x in range(lenn) ]
    data['bsortino'] = [ data['bexpected_payoff'][x] / data['bneg_std'][x] if data['bneg_std'][x]!=0 else data['bnum_trades'][x] if data['bprofit'][x]>0 else data['bnum_trades'][x] * -1 for x in range(lenn) ]
    
    
    fsplits  = [ data['ftrades'][x].split() for x in range(lenn) ]
    data['ftrades'] = [ [float(fsplits[x][y]) for y in range(len(fsplits[x]))] for x in range(len(fsplits)) ]
    data['fprofit'] = [ sum(x) for x in data['ftrades'] ]
    
    print(str(count+1)+' out of '+str(len(datas))+' done.')
    count += 1
    

# Score engineering
properties = np.array(['bprofit','bprofit_factor','bexpected_payoff','bnum_trades',
              'bsharpe','bsortino','bstd'])
num_combinations = 2**len(properties) - 1
for i in range(1,num_combinations):
    if i%int(num_combinations/20)==0:
            print('{}%'.format(round(i/num_combinations*100,0)))
    
    for dataa in datas:
        lookups = properties[[ bool(int(x)) for x in bin(i)[2:].zfill(len(properties)) ]]
        product = 1
        for j in lookups:
            product *= data[j]
        dataa['bscore{}'.format(i)] = product




# Set metaparameters
back_sets = 2 # How many previous datasets to train on?
iterations = num_files - back_sets # How many times to train and test (for i in range(iterations))?
sample_size = 1 # How many of the top predictions to take for final stats (mean and std)?
sample_start = 1 # Start at 1 for normal operation. If you only want the second recommendation set this to two and 
                 # sample_size to one.



# Go through the possible combinations of sample_starts and score_numbers and 
# set best results to results.txt

sample_starts = list(range(1,11)) # Start at 1 for normal operation. If you only want the second recommendation set this to two and 
                 # sample_size to one.
score_nums = list(range(1,num_combinations))



if 'results.txt' not in os.listdir():
    a = open('results.txt','w')
    a.close()
results_file = open('results.txt','a')
for sample_start in sample_starts:
    for score_num in score_nums:
        model_trades = []
        for i in range(num_files):
            holdout_preds = datas[i][['bscore{}'.format(score_num),'ftrades']]
            sortd = holdout_preds.sort_values('bscore{}'.format(score_num),ascending=False).iloc[sample_start-1:sample_start-1+sample_size]
            ftrades = sortd['ftrades']
            [ [model_trades.append(ftrades.iloc[x][y]) for y in range(len(ftrades.iloc[x])) ] for x in range(sample_size) ]
        
        agg_num_trades = len(model_trades)
        agg_mean = np.mean(model_trades)
        agg_std = np.std(model_trades)
        str_model_trades = ''
        for i in model_trades:
            str_model_trades += (str(i)+' ')
        
        if(agg_std>0 and agg_mean>0 and (st.norm.cdf((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5)>0.95)):
            results_file.write("Set: {0: >4}, Item: {1: >2}, Score num: {2: >3}, mean: {3: <6}, std: {4: <6}, sharpe: {5: <6}, num_trades: {6: >3}, z_score: {7: <6}, p_value: {8: <6}, profit: {9: >6}, trades: {10}\n".format(
                data_set_num,sample_start,score_num,
                round(agg_mean,4),
                round(agg_std,4),
                round(agg_mean/agg_std,4),
                round(agg_num_trades,4),
                round((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5,4),
                round(st.norm.cdf((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5),4),
                round(agg_mean*agg_num_trades,2),
                str_model_trades))

        if(agg_std>0 and agg_mean>0 and (st.norm.cdf((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5)>0.95)):
            print("Set: {0: >4}, Item: {1: >2}, Score num: {2: >3}, mean: {3: <6}, std: {4: <6}, sharpe: {5: <6}, num_trades: {6: >3}, z_score: {7: <6}, p_value: {8: <6}, profit: {9: >6}, trades: {10}\n".format(
                data_set_num,sample_start,score_num,
                round(agg_mean,4),
                round(agg_std,4),
                round(agg_mean/agg_std,4),
                round(agg_num_trades,4),
                round((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5,4),
                round(st.norm.cdf((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5),4),
                round(agg_mean*agg_num_trades,2),
                str_model_trades))

results_file.close()
print("Done writing to file")
   




## Visualization here
#
#sample_start = 4
#score_num = 84
#sample_size = 1
#
#print('\n\n\n\n\n')
#print('{},{}'.format(sample_start, score_num))
#
#model_trades     = []
#
#for i in range(num_files):
#    holdout_preds = datas[i][['bscore{}'.format(score_num),'ftrades']]
#    sortd = holdout_preds.sort_values('bscore{}'.format(score_num),ascending=False).iloc[sample_start-1:sample_start-1+sample_size]
#    ftrades = sortd['ftrades']
#    [ [model_trades.append(ftrades.iloc[x][y]) for y in range(len(ftrades.iloc[x])) ] for x in range(sample_size) ]
#
#agg_num_trades = len(model_trades)
#agg_mean = np.mean(model_trades)
#agg_std = np.std(model_trades)
#
#print("Item: {0: >2}, Score num: {1: >3}, mean: {2: <6}, std: {3: <6}, sharpe: {4: <6}, num_trades: {5: >3}, z_score: {6: <6}, p_value: {7: <6}\n".format(
#    sample_start,score_num,
#    round(agg_mean,4),
#    round(agg_std,4),
#    round(agg_mean/agg_std,4),
#    round(agg_num_trades,4),
#    round((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5,4),
#    round(st.norm.cdf((agg_mean-(-0.15))/agg_std*agg_num_trades**0.5),4)))
#
#
## Plot resultsm
#
#plt.plot(model_trades[::-1])
#plt.title('Returns')
#plt.axhline(0,c='g')
#plt.axhline(np.mean(model_trades),c='r')
#plt.show()
#model_equity = [1000]
#a = [model_equity.append(model_trades[len(model_trades)-x-1]*10+model_equity[x]) for x in range(len(model_trades))]
#plt.plot(model_equity)
#plt.title('Equity with fixed size')
#plt.show()
#print("Final Equity: {}".format(round(model_equity[-1],2)))
#model_equity = [1000]
#a = [model_equity.append(model_trades[len(model_trades)-x-1]*model_equity[x]*0.01+model_equity[x]) for x in range(len(model_trades))]
#plt.plot(model_equity)
#plt.title('Equity with percent size')
#plt.show()
#print("Final Equity: {}".format(round(model_equity[-1],2)))



