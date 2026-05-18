from enum import Enum
import os
from pathlib import Path
from typing import Generator, Iterable, Iterator, Literal, NoReturn, Optional
from functools import cached_property



class StatusCode(Enum):

    SUCCESS_WITHIN = '\tSuccess: "%s" is within the working directory'
    SUCCESS_IS = '\tSuccess: "%s" is the working directory'

    OUTSIDE = '\tError: Cannot list "%s" as it is outside the permitted working directory'
    NOT_A_DIR = '\tError: Cannot list "%s" as it is not a dir'
    NOT_A_FILE = '\tError: File not found or is not a regular file: "%s"'


    EXCEPTION = '\tError: Exception: <"%s">'

    
    @cached_property
    def error_status_codes(self) -> set['StatusCode']:
        return set([
            StatusCode.OUTSIDE,
            StatusCode.NOT_A_DIR,
            StatusCode.NOT_A_FILE,
            StatusCode.EXCEPTION
        ])
    
    @classmethod
    def is_error(cls, status_code: 'StatusCode') -> bool:
        return status_code in cls.error_status_codes


# Literal[StatusCode.SUCCESS    ,
#         StatusCode.OUTSIDE    ,
#         StatusCode.NOT_A_DIR  ,
#         StatusCode.NOT_A_FILE ,
#         StatusCode.EXCEPTION]
# # TODO is this the correct way ?
# L_S_C = Literal[StatusCode.SUCCESS    ,
#                 StatusCode.OUTSIDE    ,
#                 StatusCode.NOT_A_DIR  ,
#                 StatusCode.NOT_A_FILE ,
#                 StatusCode.EXCEPTION]

class PathItem:

    def __init__(self, abs_path: Path, size: int, is_dir: bool):
        self.abs_path = abs_path
        self.size = size
        self.is_dir = is_dir
    
    def __repr__(self) -> str:
        return 'Item <%s>' % (self.__str__(), )
    
    def __str__(self) -> str:
        if self.is_dir:
            return 'name %s: file_size=%d, is_dir=%s' % (self.abs_path, self.size, self.dir_repr)
        return 'name %s: file_size=%d, is_dir=%s' % (self.name, self.size, self.dir_repr)
    
    # Todo fix this 
    def __eq__(self, other: object, msg) -> bool:
        if not isinstance(other, PathItem):
            return NotImplemented
        
        return all([
            self.abs_path == other.abs_path,
            self.size == other.size,
            self.is_dir == other.is_dir])

    @property
    def parent_dir(self) -> NoReturn:
        raise NotImplementedError
    
    @property
    def name(self) -> str:
        return os.path.split(self.abs_path)[-1]
    
    @property
    def dir_repr(self) -> str:
        return 'True' if self.is_dir is True else 'False'


class ResultObject(tuple[bool, str]):
    # TODO **(2)** FIX name of dir_path_or_exc
    def __init__(self, 
                 status_code: StatusCode, 
                 dir_path_or_exc: Path):
        
        match status_code:

            case StatusCode.SUCCESS_WITHIN:
                self.is_error = False
                self.status_code = StatusCode.SUCCESS_WITHIN.value % (dir_path_or_exc, )
            
            case StatusCode.SUCCESS_IS:
                self.is_error = False
                self.status_code = StatusCode.SUCCESS_IS.value % (dir_path_or_exc, )
                
            case StatusCode.OUTSIDE:
                self.status_code = StatusCode.OUTSIDE.value % (dir_path_or_exc, )
                self.is_error = True
                
            case StatusCode.NOT_A_DIR:
                self.is_error = True
                self.status_code = StatusCode.NOT_A_DIR.value % (dir_path_or_exc, )
                
            case StatusCode.NOT_A_FILE:
                self.is_error = True
                self.status_code = StatusCode.NOT_A_FILE.value % (dir_path_or_exc, )
            
            case StatusCode.EXCEPTION:
                self.is_error = True
                self.status_code = StatusCode.EXCEPTION.value % (dir_path_or_exc, )

            case _:
                raise Exception('Not a valid status code.<%s>' % (status_code, ))
    
    def __iter__(self) -> Generator[str | bool, None, None]:
        yield self.is_error
        yield self.status_code


class DirInfo(tuple[ResultObject, None, list[PathItem]]):
    
    def __init__(self, 
                 result_obj: ResultObject, 
                 items: Optional[list[PathItem]]=None):
        
        self.result_obj = result_obj
        
        if not items:
            self.items = []
        else:
            self.items = items
        
    def __iter__(self) -> Iterator[ResultObject | None | list[PathItem]]:
        yield self.result_obj
        yield sorted(self.items, key=lambda l: l.size)
    
    def file_in_files(self, file_name: str) -> PathItem | None:
        """
        This function returns the file in the directory
        if it manages to find it!

        This function also has a side effect of updating the STATUS CODE 
        in case it fails to find the item.
        """
        for item in self.items:
            if file_name == item.name:
                return item
        
        # In Linux, file names and directory names are not “the same thing” conceptually, 
        # but they are treated the same at the filesystem level.
        self.update_status_code(new_status_code=StatusCode.NOT_A_FILE,
                                dir_path_or_exc=Path(file_name))

    # TODO (2)
    # def __repr__(self):
    #     return 'DirInfo<%s>' % (self.__str__())
    
    @property
    def is_err(self) -> bool:
        return self.result_obj.is_error
    
    @property
    def files_info(self):
        return '\n'.join(str(item) for item in self.items)
    
    @classmethod
    def _f_get_path(cls, path: Path) -> Path:
        return Path(os.path.abspath(os.path.normpath(path)))
    
    @classmethod
    def get_files_info(cls, 
                       working_directory: Path, 
                       dest_directory: str) -> 'DirInfo':
        """
        Factory method to generate a DirInfo object.
        """
        # print(f"""Result for {'current' if dest_directory == '.' else f"'{dest_directory}'"} directory:""")
        
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, dest_directory))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return DirInfo(result_obj=ResultObject(status_code=StatusCode.OUTSIDE,
                                                   dir_path_or_exc=dest_directory))

        parts = os.path.split(os.path.join(os.getcwd(), working_directory))
        prefix, suffix = parts[0], parts[1]

        
        def connect_d_to_d(p_dir: Path) -> Optional[Path]:
            
            if dest_directory == p_dir:
                return Path(os.path.join(prefix, p_dir))
            
            for _, dirs, _ in os.walk(p_dir):
                
                for _dir in dirs:
                    
                    full_path = Path(os.path.join(prefix, p_dir, _dir))
                
                    # found target directory  
                    if dest_directory == _dir:
                        return Path(full_path)

                    # dfs recursion
                    res = connect_d_to_d(p_dir=full_path)
                    if res:
                        return Path(res)
            return None

        status_code = StatusCode.SUCCESS_WITHIN
        if dest_directory == str(Path(".")):
            status_code = StatusCode.SUCCESS_IS
            dest_directory = Path(suffix)
        else:
            # try to connect working_directory to dest_directory
            working_directory = connect_d_to_d(p_dir=working_directory)
        
        if working_directory is None:
            return DirInfo(result_obj=ResultObject(status_code=StatusCode.NOT_A_DIR,
                                                       dir_path_or_exc=dest_directory))

        
        files_info = DirInfo(result_obj=ResultObject(status_code=status_code,
                                                     dir_path_or_exc=dest_directory))
        
        # TODO update
        # for root, dirs, files in os.walk(new_directory):
        for file_or_item in os.listdir(working_directory):
            file_path = os.path.join(working_directory, Path(file_or_item))
            files_info.items.append(PathItem(abs_path=Path(file_path),
                                             size=os.path.getsize(file_path),
                                             is_dir=os.path.isdir(file_path)))

        return files_info

    # TODO **(2)** FIX name of dir_path_or_exc
    def update_status_code(self, 
                           new_status_code: Literal[StatusCode.SUCCESS_WITHIN ,
                                                    StatusCode.SUCCESS_IS     ,
                                                    StatusCode.OUTSIDE        ,
                                                    StatusCode.NOT_A_DIR      ,
                                                    StatusCode.NOT_A_FILE     ,
                                                    StatusCode.EXCEPTION]     ,
                           dir_path_or_exc: Path | Exception) -> None:
        
        self.result_obj.status_code = new_status_code % (dir_path_or_exc, )
        self.result_obj.is_error = StatusCode.is_error(status_code=new_status_code)
