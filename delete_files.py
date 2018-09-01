
import os
import re


data_hub_file_path = 'C:\\Users\\Dell\\Desktop\\PythonAlgoFolder\\DataHub'
batch_file_paths = ["C:/Program Files (x86)/OANDA - MetaTrader",
              "C:/Program Files (x86)/OANDA - MetaTrader - Copy",
              "C:/Program Files (x86)/OANDA - MetaTrader - Copy (2)"]
params_sets_file_paths = ["C:/Program Files (x86)/OANDA - MetaTrader/tester",
                          "C:/Program Files (x86)/OANDA - MetaTrader - Copy/tester",
                          "C:/Program Files (x86)/OANDA - MetaTrader - Copy (2)/tester"]


for i in range(3):
    
    os.chdir(batch_file_paths[i])
    try:
        os.remove('batch_backtests.bat')
    except Exception:
        pass
    
    os.chdir(params_sets_file_paths[i])
    regex = re.compile('iter*')
    [os.remove(f) for f in os.listdir() if re.match(regex,f)]
    
    os.chdir(data_hub_file_path)
    try:
        os.remove('master_batch_file.bat')
    except Exception:
        pass
    
    os.chdir(params_sets_file_paths[i]+'/files')
    [os.remove(f) for f in os.listdir() if '.csv' in f]