

import os
import sys
from filepaths import filepaths as fps

filepaths = fps()

data_hub_file_path = filepaths['DataHub']
back_file_path = filepaths['Back']
live_file_path = filepaths['Live']
ini_file_paths = [filepaths['MT-1tester'],filepaths['MT-2tester'],
                  filepaths['MT-3tester']]


try:
    genetic = int(sys.argv[1])
except Exception:
    genetic = 1
    
for i in range(3):
    os.chdir(ini_file_paths[i])
    os.remove('EchoDiscreteModelMaker.ini')
    
    ini_file = open('EchoDiscreteModelMaker.txt','a')
    ini_contents = '''<common>
positions=2
deposit=1000
currency=USD
fitnes=5
genetic={}
</common>\n
<inputs>
Long_Back_1=0
Long_Back_1,F=1
Long_Back_1,1=1
Long_Back_1,2=1
Long_Back_1,3=96
Long_Back_2=0
Long_Back_2,F=1
Long_Back_2,1=1
Long_Back_2,2=1
Long_Back_2,3=96
Short_Back_1=0
Short_Back_1,F=1
Short_Back_1,1=1
Short_Back_1,2=1
Short_Back_1,3=96
Short_Back_2=0
Short_Back_2,F=1
Short_Back_2,1=1
Short_Back_2,2=1
Short_Back_2,3=96
Open_Bars=0
Open_Bars,F=1
Open_Bars,1=1
Open_Bars,2=1
Open_Bars,3=24
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
split_datetime=1527120000
split_datetime,F=0
split_datetime,1=0
split_datetime,2=0
split_datetime,3=0
write_to_file=1
write_to_file,F=0
write_to_file,1=0
write_to_file,2=1
write_to_file,3=1
file_name_prefix=1
file_name_prefix,F=0
file_name_prefix,1=0
file_name_prefix,2=0
file_name_prefix,3=0
score_type=0
score_type,F=0
score_type,1=0
score_type,2=0
score_type,3=0
Lots=0.01000000
Lots,F=0
Lots,1=0.00000000
Lots,2=0.00000000
Lots,3=0.00000000
get_random_results=1
get_random_results,F=0
get_random_results,1=0
get_random_results,2=1
get_random_results,3=1
</inputs>\n
<limits>
balance_enable=0
balance=200.00
profit_enable=0
profit=10000.00
marginlevel_enable=0
marginlevel=30.00
maxdrawdown_enable=0
maxdrawdown=70.00
consecloss_enable=0
consecloss=5000.00
conseclossdeals_enable=0
conseclossdeals=10.00
consecwin_enable=0
consecwin=10000.00
consecwindeals_enable=0
consecwindeals=30.00
</limits>'''.format(genetic)
    
    ini_file.write(ini_contents)
    ini_file.close()
    os.rename('EchoDiscreteModelMaker.txt','EchoDiscreteModelMaker.ini')
    

    


