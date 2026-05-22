import os
from collections.abc import Iterator
from enum import Enum
from functools import cached_property, partial
from pathlib import Path
from typing import Callable, Optional, Self

from functions.consts import CWD, DOT

# TODO **3** consider updating to have list of messages on levels (or res objects) / updating status
# TODO FIX string literals / anots
# TODO current implementation propably fails on dotted file names.
# TODO UPDATE PathItem with relative path as well

class StatusCode(Enum):

    SUCCESS_DIR_WITHIN = '\tSuccess: "%s" is within the working directory'
    SUCCESS_DIR_IS = '\tSuccess: "%s" is the working directory'
    SUCCESS_FILE_FOUND = '\tSuccess: file "%s" found'

    NOT_A_DIR = '\tError: Cannot list "%s" as it is not a dir'

    FILE_NOT_FOUND = '\tError: File not found or is not a regular file: "%s"'

    # !? security considerations 
    DIR_DOES_NOT_EXIST = '\tError: Failed to find dir "%s" as it does not exist' 

    OUTSIDE = '\tError: Cannot list "%s" as it is outside the permitted working directory'

    EXCEPTION = '\tError: Exception: <"%s">' # not tested

    EMPTY = '\tEmpty <"%s">' #?

    @classmethod
    def abort_status_codes(cls) -> set['StatusCode']:
        return set([
            StatusCode.OUTSIDE,
            StatusCode.EXCEPTION,
            StatusCode.EMPTY,
            StatusCode.DIR_DOES_NOT_EXIST,
            StatusCode.FILE_NOT_FOUND,
            StatusCode.EXCEPTION
        ])
    
    @classmethod
    def permit_write_status_codes(cls) -> set['StatusCode']:
        return set([
            StatusCode.SUCCESS_DIR_WITHIN,
            StatusCode.SUCCESS_DIR_IS,
            StatusCode.SUCCESS_FILE_FOUND,
            StatusCode.NOT_A_DIR,
        ])
    
    @classmethod
    def is_error(cls, status_code: 'StatusCode') -> bool:
        return status_code in cls.abort_status_codes()

    @classmethod
    def formatted_msg(cls, status_code: 'StatusCode', raw_msg: str) -> str:
        
        match status_code:
            
            case StatusCode.DIR_DOES_NOT_EXIST:
                return StatusCode.DIR_DOES_NOT_EXIST.value % (raw_msg, )
            
            case StatusCode.SUCCESS_DIR_WITHIN:
                return StatusCode.SUCCESS_DIR_WITHIN.value % (raw_msg, )
            
            case StatusCode.SUCCESS_DIR_IS:
                return StatusCode.SUCCESS_DIR_IS.value % (raw_msg, )
            
            case StatusCode.SUCCESS_FILE_FOUND:
                return StatusCode.SUCCESS_FILE_FOUND.value % (raw_msg, )
                
            case StatusCode.OUTSIDE:
                return StatusCode.OUTSIDE.value % (raw_msg, )
                
            case StatusCode.NOT_A_DIR:
                return StatusCode.NOT_A_DIR.value % (raw_msg, )
                
            case StatusCode.FILE_NOT_FOUND:
                return StatusCode.FILE_NOT_FOUND.value % (raw_msg, )
            
            case StatusCode.EXCEPTION:
                return StatusCode.EXCEPTION.value % (raw_msg, )
            
            case StatusCode.EMPTY:
                #?
                return StatusCode.EMPTY.value % (raw_msg, )

            case _:
                raise Exception('Not a valid status code.<%s>' 
                                % (status_code, ))


class PathItem:

    def __init__(self, 
                 abs_path: Path,
                 size: int, 
                 is_dir: bool):
        self.abs_path = abs_path
        self.size = size
        self.is_dir = is_dir
    
    def __repr__(self) -> str:
        return 'Item <%s>' % (self.__str__(), )
    
    def __str__(self) -> str:
        if self.is_dir:
            return 'name %s: file_size=%d, is_dir=%s' % (self.abs_path, self.size, self.dir_repr)
        return 'name %s: file_size=%d, is_dir=%s' % (self.file_name, self.size, self.dir_repr)
    
    # TODO fix msg
    def __eq__(self, other: object, /, msg) -> bool:
        if not isinstance(other, PathItem):
            return NotImplemented
        
        return all([
            self.abs_path == other.abs_path,
            self.size == other.size,
            self.is_dir == other.is_dir])

    @cached_property
    def _full_file_name_parts(self) -> tuple[str, str]:
        return os.path.split(self.abs_path)
    
    @cached_property
    def parent_dir(self) -> str:
        return self._full_file_name_parts[0]
    
    @cached_property
    def file_name(self) -> str:
        return self._full_file_name_parts[1]
    
    @cached_property
    def _file_name_parts(self) -> list[str]:
        assert DOT in self.file_name
        return self.file_name.split(DOT)
    
    @cached_property
    def stem(self) -> str:
        return self._file_name_parts[0]
    
    @cached_property
    def ext(self) -> str:
        return self._file_name_parts[1]

    @property
    def dir_repr(self) -> str:
        return 'True' if self.is_dir is True else 'False'
    

# TODO maybe ResultObject should inherit from levels and yield lists?
class ResultObject(tuple[bool, StatusCode, str]):
    
    def __init__(self, 
                 status_code: StatusCode, 
                 raw_msg: str | Exception) -> None:
        
        if isinstance(raw_msg, Path):
            1/0

        self.is_error = status_code in StatusCode.abort_status_codes()
        self.status_code = status_code

        if isinstance(raw_msg, str):
            self.raw_msg = StatusCode.formatted_msg(status_code=status_code, 
                                                    raw_msg=raw_msg)
        if isinstance(raw_msg, Exception):
            self.raw_msg = StatusCode.formatted_msg(status_code=status_code, 
                                                    raw_msg=raw_msg)
        
    def __iter__(self) -> Iterator[bool | StatusCode | str, None]:
        yield self.is_error
        yield self.status_code
        yield self.raw_msg

    def update_status(self, new_status_code: 
                      StatusCode, new_msg: str | Exception) -> None:
        
        if isinstance(new_msg, Path):
            1/0

        self.status_code = new_status_code
        self.is_error = new_status_code in StatusCode.abort_status_codes()
        self.raw_msg = StatusCode.formatted_msg(status_code=new_status_code, 
                                                raw_msg=new_msg)


# TODO is this the correct way to do the iter ?
class DirInfo(tuple[ResultObject, list[PathItem]]):
    """
    In order to initialize this class
    # If you pass the dest_directory as empty string the 
    # current working directory will be used instead
    1. Either pass the working directory along with the nested directory
       to get the directory info
    2. To get the file metadata, use the flag search_for_file
       and then use the file_in_files function. 
    """
    # TODO this seems bad ... workaround for now
    def __new__(cls, *args, **kwargs) -> Self:
        obj = super().__new__(cls)

        if 'result_obj' in kwargs:
            obj.result_obj = kwargs['result_obj']
            assert 'items' in kwargs
            obj.items = []
            return 
        
        return super().__new__(cls)
    
    def __init__(self, 
                 working_directory: Path, 
                 dest_directory: str) -> None:
        
        if isinstance(dest_directory, Path):
            1/0
            
        assert DOT not in str(working_directory)
        
        if not dest_directory:
            dest_directory = DOT

        # Safe keep those, since we may need them later
        self.working_directory = working_directory
        self.dest_directory = dest_directory
        
        self.result_obj = None
        self.items: list[PathItem] = []

        self._get_files_info()
        assert self.result_obj != None
    
    def __iter__(self) -> Iterator[ResultObject | list[PathItem], None]:
        yield self.result_obj
        yield sorted(self.items, key=lambda l: l.size)
    
    @property
    def files_info(self):
        return '\n'.join(str(item) for item in self.items)

    @classmethod
    def _f_get_path(cls, path: Path) -> Path:
        return Path(os.path.abspath(os.path.normpath(path)))
    
    def _get_files_info(self) -> None:
        """
        Initializer helper method
        """
        working_directory = self.working_directory
        dest_directory = self.dest_directory

        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, dest_directory))

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            self.result_obj=ResultObject(status_code=StatusCode.OUTSIDE,
                                         raw_msg=dest_directory)
            return

        working_parts = os.path.split(os.path.join(os.getcwd(), working_directory))
        master_prefix, master_suffix = working_parts

        dest_parts = os.path.split(dest_directory)
        dest_prefix, dest_suffix = dest_parts
        

        def connect_d_to_d(p_dir: Path) -> Optional[Path]:
            
            parts = str(p_dir).partition(dest_directory)
            found_dir = sum(map(lambda x: x is str(), parts)) == 1
            found_dir |= os.path.normpath(dest_directory) == dest_prefix

            if found_dir:
                return Path(os.path.join(master_prefix, p_dir))
            
            for _, dirs, _ in os.walk(p_dir):

                for _dir in dirs:
                    full_path = Path(os.path.join(master_prefix, p_dir, _dir))

                    res = connect_d_to_d(p_dir=full_path)
                    if res:
                        return res

        if dest_directory == DOT:
            connected_directory = working_directory
            self.result_obj = ResultObject(status_code=StatusCode.SUCCESS_DIR_IS,
                                           raw_msg=DOT)
        else:
            # try to connect working_directory to dest_directory
            connected_directory = connect_d_to_d(p_dir=working_directory)

            if not connected_directory:
                self.result_obj = ResultObject(status_code=StatusCode.NOT_A_DIR,
                                               raw_msg=dest_directory)
                return 

            self.result_obj = ResultObject(status_code=StatusCode.SUCCESS_DIR_WITHIN,
                                           raw_msg=dest_directory)

        # TODO update
        # for root, dirs, files in os.walk(new_directory):
        for file_or_item in os.listdir(connected_directory):

            file_path = os.path.join(connected_directory, Path(file_or_item))

            path_item = PathItem(abs_path=Path(file_path),
                                 size=os.path.getsize(file_path),
                                 is_dir=os.path.isdir(file_path))
            
            self.items.append(path_item)

    def file_in_files(self, file_name: str) -> PathItem | None:
        """
        This function returns the file in the directory
        if it manages to find it!

        This function also has a side effect of updating the STATUS CODE 
        in case it fails or succeeds to find the file.
        """
        print(' [*] searching item ======> ', file_name)
        for item in self.items:
            
            if file_name == item.file_name:
                
                self.result_obj.update_status(new_status_code=StatusCode.SUCCESS_FILE_FOUND,
                                              new_msg=file_name)
                return item
        
        # In Linux, file names and directory names are not “the same thing” conceptually, 
        # but they are treated the same at the filesystem level.
        self.result_obj.update_status(new_status_code=StatusCode.FILE_NOT_FOUND,
                                      new_msg=file_name)


def _get_files_info(working_directory: Path, 
                    directory: str) -> tuple[ResultObject, 
                                             tuple[Optional[PathItem], Optional[str]]]:
    
    head, tail = os.path.split(directory)

    dir_info = DirInfo(working_directory=working_directory, 
                       dest_directory=head if '.' in tail else directory)

    (err, status, msg), files_info = dir_info

    return (err, status, msg), files_info


def get_files_info(directory: str) -> Callable:
    return partial(_get_files_info, working_directory=Path(CWD))
