import os
from pathlib import Path

from functions.get_file_contents import _get_file_contents
from functions.get_files_info import ResultObject, StatusCode


def _write_file(working_directory: Path, 
                file_path: str, 
                content: str) -> tuple[ResultObject, str]:
    
    try:
        
        _file_path = os.path.join(os.getcwd(), working_directory, file_path)
        (___file_path, file_ext) = os.path.split(_file_path)

        if os.path.exists(___file_path) and not file_ext:
            res_object = ResultObject()
            res_object.update_status(new_status_code=res_object.status_code,
                                     new_msg=f'Error: Cannot write to "{file_path}" as it is a directory')
            return res_object, ''


        res_object, (file, contents, ) = _get_file_contents(working_directory=working_directory, 
                                                            file_path=file_path)
        (err, status, msg) = res_object
        
        if err:
            if status != StatusCode.FILE_NOT_FOUND:
                return res_object, ''
        
        
        try:
            os.makedirs(___file_path, exist_ok=True)
        except OSError:
            # Ignore this error since the file will be overwritten.
            # Maybe we want to delete the file before recreating it?
            ...

        with open(_file_path, 'w') as f:
            f.write(content)

        # Here we dont update status for now
        return (err, status, f'Successfully wrote to "{file_path}" ({len(content)} characters written)'), content # type: ignore[return-value]

    except Exception as e:
        result_object = ResultObject(status_code=StatusCode.EXCEPTION,
                                     raw_msg=e)
        return result_object, ''
