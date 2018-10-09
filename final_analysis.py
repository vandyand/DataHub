

import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from filepaths import filepaths as fps

filepaths = fps()

data_hub_file_path = filepaths['DataHub']
back_file_path = filepaths['Back']


print("Running final_analysis.py...")

os.chdir(data_hub_file_path)

hyper_lines_per_iterator = 40

hyper_iterators = int(sum(1 for line in open('hyperparameters.txt'))/hyper_lines_per_iterator)

contents = open('hyperparameters.txt','r+').read()
content = []
for i in contents.split('\n'):
    content.append(i.split(' = '))

data_set_nums = [ int(content[17+hyper_lines_per_iterator*hyper_iterator][1]) for hyper_iterator in range(hyper_iterators) ]




os.chdir(back_file_path)

results = []
# This is for finding the best score & item out of all analyzed scores & items
# in all the sets that were ever run.
#for i in [ j for j in os.listdir() if 'Set' in j and '.' not in j ]:
#    results.append(open(back_file_path+'\\{}\\results.txt'.format(i)).read())

#set_num = 10
for data_set_num in data_set_nums:
    results.append(open(back_file_path+'\\Set{}\\results.txt'.format(data_set_num)).read())

cols = ['set','item','score','mean','std','sharpe','num_trades','z_score','p_value','profit','trades']
data = pd.DataFrame(columns = cols)
for i in range(len(results)):
    # I made this super compact and confusing so no one knows what it does. Good idea eh?
    data = data.append(pd.DataFrame([ j.split(',') for j in re.sub('[A-Za-z_:]','',results[i]).split('\n')[:-1] ],columns=cols))

data['trades'] = [ [ float(i) for i in data.iloc[x]['trades'].split() ] for x in range(data.shape[0]) ]

data = data.sort_values(['z_score','item'],ascending=[False,True])

print(data.head(20))

try:

    model_trades = data['trades'].iloc[0]
    model_equity = [1000]
    a = [model_equity.append(model_trades[x]*10+model_equity[x]) for x in range(len(model_trades))]
    plt.plot(model_equity)
    plt.title('Equity with fixed size')
    plt.show()
    print("Final Equity: {}".format(round(model_equity[-1],2)))
    model_equity = [1000]
    a = [model_equity.append(model_trades[x]*model_equity[x]*0.01+model_equity[x]) for x in range(len(model_trades))]
    plt.plot(model_equity)
    plt.title('Equity with percent size')
    plt.show()
    print("Final Equity: {}".format(round(model_equity[-1],2)))
    
    print(data.iloc[0][['set','item','score']])

except Exception:
    data = pd.DataFrame(np.array([[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]).T,columns=data.columns) 

os.chdir(back_file_path)

final_results_file_name = 'final_results-Set{}.txt'.format(data_set_num)

open(final_results_file_name,'w').close()
with open(final_results_file_name,'a') as f:
    f.write('set, item, score\n{},{},{}'.format(data.iloc[0,0],data.iloc[0,1],data.iloc[0,2]))


