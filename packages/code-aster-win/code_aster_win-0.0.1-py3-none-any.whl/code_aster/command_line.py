import code_aster as ca
import sys

def py_as_run(file_path, options: list = []):
    args = sys.argv[1:]
    if len(args) < 1:
        print('Please provide a path to a export file.')
    else:
        print(args)
        #ca.as_run(file_path,options)

def py_run_astk():
    ca.run_astk()