python ini_genetic_param.py 1
python copy_eas.py

python delete_files.py
python big_master_backtests_generator.py 21
start /wait "" "master_batch_file.bat"

python golf_analysis.py 21
python final_analysis.py