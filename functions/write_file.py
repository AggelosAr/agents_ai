
from pathlib import Path

from functions.get_file_content import get_file_contents
import os 
import shutil


def write_file(working_directory: Path, 
               file_path: Path, 
               content: str) -> tuple[str, str | None]:
    try:
        
        _file_path = os.path.join(os.getcwd(), working_directory, file_path)
        (___file_path, file_ext) = os.path.split(_file_path)

        if os.path.exists(___file_path) and not file_ext:
            return f'Error: Cannot write to "{file_path}" as it is a directory', None


        contents, ((err, status), files_info) = get_file_contents(working_directory=working_directory, 
                                                                  file_path=file_path)
        
        if err:
            return contents, None
        
        if os.path.exists(_file_path):
            shutil.rmtree(_file_path)

        os.makedirs(_file_path, exist_ok=True)
        
        with open(_file_path, 'w') as f:
            f.write(contents)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)', contents

    except Exception as e:
        return f'\tError: {str(e)}', None
       