import os
from pathlib import Path
from typing import Generator


class Item:

    def __init__(self, abs_path: Path, size: int, is_dir: bool):
        self.abs_path = abs_path
        self.size = size
        self.is_dir = is_dir
    
    def __repr__(self):
        return 'Item [%s]<%s>' % (self.abs_path, self.__str__())
    
    def __str__(self):
        return 'name %s: file_size=%d, is_dir=%s' % (self.name, self.size, self.dir_repr)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        
        return all([
            self.abs_path == other.abs_path,
            self.size == other.size,
            self.is_dir == other.is_dir])

    @property
    def name(self) -> Path:
        return os.path.split(self.abs_path)[-1]
    
    @property
    def dir_repr(self) -> str:
        return 'True' if self.is_dir is True else 'False'


class ResultObject(tuple[bool, str]):
    
    def __init__(self, is_error: bool, status: str):
        self.is_error = is_error
        self.status = status

    def __iter__(self) -> Generator[bool | str, None]:
        yield self.is_error
        yield self.status


class DirInfo(tuple[ResultObject, list[Item]]):
    
    get_path = lambda p: os.path.abspath(os.path.normpath(p))

    def __init__(self, result_code: str, items: list[Item]=[]):
        self.result_code = result_code
        self.items = items
    
    def __iter__(self) -> Generator[ResultObject | list[Item], None]:
        yield self.result_object
        yield sorted(self.items, key=lambda l: l.size)
    
    def file_in_files(self, target: str) -> Item | None:
        for item in self.items:
            if target == item.name:
                return item

    # TODO (2)
    # def __repr__(self):
    #     return 'DirInfo<%s>' % (self.__str__())
    
    @property
    def result_object(self) -> ResultObject:
        return ResultObject(is_error=self.is_error, status=self.result_code)
    
    @property
    def is_error(self) -> bool:
        return self.result_code and '\tError' == self.result_code[:6]
    
    @property
    def files_info(self):
        return '\n'.join(str(item) for item in self.items)
    
    @classmethod
    def get_files_info(cls, working_directory: Path, dest_directory: Path=".") -> 'DirInfo':
        """
        returns A tuple containing the result code: str and a list of items
        """
        # print(f"""Result for {'current' if dest_directory == '.' else f"'{dest_directory}'"} directory:""")

        #!
        #dest_directory = os.path.split(dest_directory)[0]
        #!

        parts = os.path.split(os.path.join(os.getcwd(), working_directory))
        prefix, suffix = parts[0], parts[1]
        if dest_directory == '.' or not dest_directory:
            dest_directory = suffix

        def connect_d_to_d(p_dir: str) -> str | None:
            
            if dest_directory == p_dir:
                return os.path.join(prefix, p_dir) 
            
            for _, dirs, _ in os.walk(p_dir):
                
                for _dir in dirs:
                    
                    
                    full_path = os.path.join(prefix, p_dir, _dir) 
                
                    # found target directory  
                    if dest_directory == _dir:
                        return full_path

                    # dfs recursion
                    res = connect_d_to_d(p_dir=full_path)
                    if res:
                        return res
        
        # try to connect working_directory to dest_directory
        new_directory = connect_d_to_d(p_dir=working_directory)
        
        if new_directory is None:
            j_path = os.path.join(cls.get_path(working_directory), cls.get_path(dest_directory))
            if len(j_path) > len(working_directory):
                return DirInfo(result_code=f'\tError: Cannot list "{dest_directory}" as it is outside the permitted working directory')
            
            return DirInfo(result_code=f'\tError: Cannot list "{dest_directory}" as it is outside the permitted working directory')

        
        files_info = DirInfo(result_code=f'\tSuccess: "{dest_directory}" is within the working directory')

        for file_or_item in os.listdir(new_directory):
            file_path = os.path.join(new_directory, file_or_item)
            files_info.items.append(Item(abs_path=file_path,
                                         size=os.path.getsize(file_path),
                                         is_dir=os.path.isdir(file_path)))

        return files_info
