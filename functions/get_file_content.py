from pathlib import Path
from typing import Optional

from functions.get_files_info import DirInfo
import os


MAX_CHARS = 10_000


# -> tuple[str, Optional[tuple[bool, str]], Optional[list[Item]]]:
def get_file_contents(working_directory: Path, file_path: Path) -> tuple[str, Optional[DirInfo]]:

    try:

        dir_info = DirInfo(result_code='')

        dest_root = os.path.split(file_path)
        dest_root, target_name = dest_root

        if not dest_root:
            dest_root = '.'

        (err, status), files_info = dir_info.get_files_info(working_directory=working_directory, 
                                                            dest_directory=dest_root)

        # TODO maybe use the error and propagate it further back ?
        if err:
            return f'\tError: Cannot read "{file_path}" as it is outside the permitted working directory', None, None, None
        
        
        file_found = dir_info.file_in_files(target=target_name)

        if not file_found:
            return f'\tError: File not found or is not a regular file: "{file_path}"', None, None, None


        with open(file_found.abs_path, 'r') as f:
            contents  = f.read(MAX_CHARS)

            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return contents, (err, status), files_info
        
    except Exception as e:
        return f'\tError: {str(e)}', None, None, None
       