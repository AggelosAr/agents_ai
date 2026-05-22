import os
import subprocess
from pathlib import Path

from functions.consts import PROC_TIMEOUT
from functions.get_file_content import get_file_contents
from functions.get_files_info import StatusCode

# TODO FILL StatusCode.EMPTY and maybe use the result object here as well?
# https://docs.python.org/3/library/subprocess.html#security-considerations or exc?
# TODO assert args

def run_python_file(working_directory: str, 
                    file_path: str, 
                    args: list[str] | None = None) -> str:
    
    try: 

        _file_path = os.path.join(os.getcwd(), working_directory, file_path)
        ___file_path, file_ext = os.path.split(_file_path)

        if '.py' not in file_ext:
            return f'Error: "{file_path}" is not a Python file'

        res = get_file_contents(working_directory=Path(working_directory), 
                                file_path=file_path)
        
        (err, status, msg), (file, contents, ) = res


        if err:

            match status:

                case StatusCode.OUTSIDE:
                    return 'Cannot execute "%s" as it is outside' % (file_path, )
                
                case StatusCode.FILE_NOT_FOUND:
                    return '"%s" does not exist' % (file_path, )
                
            return msg
        
        # workaround
        assert file

        # TODO 
        # assert we are inside the .venv dir
        # then cd to the cwd

        print( ' ________________________________________________________________________ ')
        if args:
            command = ('cd %s && python3 -m %s %s' 
            % (file.parent_dir, file.stem, ' '.join(map(lambda x: '"%s"' % (x, ), args)), ))
        else:
            command = 'cd %s && python3 -m %s' % (file.parent_dir, file.stem, )
              
        print('\t\tEXCECUTING: %s' % (command, ))
        print( ' ________________________________________________________________________ ')

        commands = [*command]
        
        completed_process = None
        try:
            # Set the working directory properly.
            completed_process = subprocess.run(command, 
                                               timeout=PROC_TIMEOUT, 
                                               text=True, 
                                               capture_output=True,
                                               shell=True)
        except subprocess.TimeoutExpired:
            ...

        assert completed_process
        
        result_string = [' | ']

        if completed_process.returncode != 0:
            result_string.append(' | -> Process exited with code %d' % (completed_process.returncode, ))

        if completed_process.stdout == completed_process.stderr:
            result_string.append(' | -> No output produced')

        if completed_process.stdout:
            result_string.append(' | -> STDOUT: %s' % (completed_process.stdout, ))
        
        if completed_process.stderr:
            result_string.append(' | -> STDERR: %s' % (completed_process.stderr, ))

        return '\n'.join(result_string)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'
