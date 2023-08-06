import subprocess
from pathlib import Path

cwd = Path(__file__).parent.absolute()


def as_run(file_path: Path, options: list = []):
    print('Running code_aster. Please wait')
    cmd = str((cwd / Path('code-aster_v2019_std-win64/v2019/bin/as_run.bat')).absolute())
    print(cmd,str(file_path))
    process = subprocess.run([cmd,str(file_path)]+options,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True
                             )
    print('Finished simulation')
    return process

def run_astk( options: list = []):
    cmd = str(cwd / Path('code-aster_v2019_std-win64/v2019/bin/as_launch.exe'))
    print(cmd)
    process = subprocess.run([cmd]+options,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True
                             )

    return process

def test_installation():
    test_file = str((cwd / Path('code-aster_v2019_std-win64/example/forma01a.export')).absolute())
    return as_run(test_file)