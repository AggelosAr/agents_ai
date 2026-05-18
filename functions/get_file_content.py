from pathlib import Path
from typing import Optional

from functions.get_files_info import DirInfo, ResultObject, StatusCode
import os


MAX_CHARS = 10_000



def get_file_contents(working_directory: Path, 
                      file_path: Path) -> tuple[ResultObject, 
                                                tuple[Optional[str]]]:

    try:

        head, tail = os.path.split(file_path)
       
        # (err, status), files_info = DirInfo.get_files_info(working_directory=working_directory, 
        #                                                    dest_directory=Path(dest_root))
        dir_info = DirInfo.get_files_info(working_directory=working_directory,
                                          dest_directory=head if head else '.')
      
        (err, status), files_info = dir_info

        if err:
            return dir_info.result_obj, (None, )
        
        file_found = dir_info.file_in_files(file_name=tail)

        if not file_found:
            return dir_info.result_obj, (None, )


        with open(file_found.abs_path, 'r') as f:
            contents  = f.read(MAX_CHARS)

            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return dir_info.result_obj, (contents, )
        
    except Exception as e:
        dir_info.update_status_code(new_status_code=StatusCode.EXCEPTION,
                                    dir_path_or_exc=str(e))
        return dir_info.result_obj, (None, )
       