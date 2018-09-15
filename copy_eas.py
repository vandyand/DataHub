


import shutil
from filepaths import filepaths as fps

filepaths = fps()

ea_paths = [filepaths['MT-1Experts'],filepaths['MT-1Experts'],
            filepaths['MT-1Experts']]

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




