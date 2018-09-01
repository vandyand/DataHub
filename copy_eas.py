


import shutil

ea_paths = [
        "C:/Program Files (x86)/OANDA - MetaTrader/MQL4/Experts",
        "C:/Program Files (x86)/OANDA - MetaTrader - copy/MQL4/Experts",
        "C:/Program Files (x86)/OANDA - MetaTrader - copy (2)/MQL4/Experts"]

#try:
#    shutil.rmtree(ea_paths[1])
#except Exception:
#    pass
#try:
#    shutil.rmtree(ea_paths[2])
#except Exception:
#    pass

shutil.rmtree(ea_paths[1])
shutil.rmtree(ea_paths[2])

shutil.copytree(ea_paths[0],ea_paths[1])
shutil.copytree(ea_paths[0],ea_paths[2])




