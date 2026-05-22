from functools import partial
import os
from pathlib import Path
from typing import Callable, Optional

from functions.consts import CWD
from functions.get_file_contents import _get_file_contents
from functions.get_files_info import ResultObject, StatusCode


# def write_file(file_path: str = '', content: str = '') -> Callable:
#     return partial(_write_file, Path(CWD))(file_path, content)


# TODO update when/if list of messages is added
def _write_file(working_directory: Path, 
                file_path: str, 
                content: str) -> tuple[ResultObject, Optional[str]]:
    
    try:
        
        _file_path = os.path.join(os.getcwd(), working_directory, file_path)
        (___file_path, file_ext) = os.path.split(_file_path)

        if os.path.exists(___file_path) and not file_ext:
            return (True, StatusCode.EMPTY, f'Error: Cannot write to "{file_path}" as it is a directory'), None


        (err, status, msg), old_content = _get_file_contents(working_directory=working_directory, 
                                                            file_path=file_path)
        
        if err:
            if status != StatusCode.FILE_NOT_FOUND:
                return (err, status, msg), None
        
        
        try:
            os.makedirs(___file_path, exist_ok=True)
        except OSError:
            # Ignore this error since the file will be overwritten.
            # Maybe we want to delete the file before recreating it?
            ...

        with open(_file_path, 'w') as f:
            f.write(content)

        # Here we dont update status for now
        return (err, status, f'Successfully wrote to "{file_path}" ({len(content)} characters written)'), content

    except Exception as e:
        result_object = ResultObject(status_code=StatusCode.EXCEPTION,
                                     raw_msg=str(e))
        return result_object, (None, )
