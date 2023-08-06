import code_aster as ca
from pathlib import Path
path = Path('C:/Users/daniel.steinegger/Documents/Coding/CodeAster_pkg/Windows/code_aster/code-aster_v2019_std-win64/example/forma01a.export')
logs = ca.as_run(path)
print(logs.stdout)