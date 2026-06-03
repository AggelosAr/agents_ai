import os
from pathlib import Path
from typing import Optional

from functions.consts import MAX_CHARS
from functions.get_files_info import (DirInfo, PathItem, ResultObject,
                                      StatusCode)


def _get_file_contents(working_directory: Path, 
                       file_path: str) -> tuple[ResultObject, 
                                                tuple[Optional[PathItem], str]]:
    try:

        head, tail = os.path.split(file_path)

        # TODO refactor maybe !!!!
        # Force get_files_info to search in the parent dir 
        # since how further logic is implemented 
        dir_info = DirInfo(working_directory=working_directory, 
                           dest_directory=head if '.' in tail else file_path)

        (err, status, msg), files_info = dir_info

        if err:
            dir_info.result_obj.update_status(new_status_code=status,
                                              new_msg=file_path)
            
            return dir_info.result_obj, (None, '', )
        
        file_found = dir_info.file_in_files(file_name=tail if '.' in tail else '')
        
        if not file_found:
            return dir_info.result_obj, (None, '', )


        with open(file_found.abs_path, 'r') as f:
            contents  = f.read(MAX_CHARS)

            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return dir_info.result_obj, (file_found, contents, )
                
    except Exception as e:
        result_object = ResultObject(status_code=StatusCode.EXCEPTION,
                                     raw_msg=str(e))
        return result_object, (None, '', )
