
import os
import re
from filepaths import filepaths as fps

filepaths = fps()

data_hub_file_path = filepaths['DataHub']
batch_file_paths = [filepaths['MT-7'],filepaths['MT-8'],filepaths['MT-9']]
params_sets_file_paths = [filepaths['MT-7tester'],filepaths['MT-8tester'],
                          filepaths['MT-9tester']]


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