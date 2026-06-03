import unittest
from pathlib import Path

from functions.get_files_info import DirInfo, PathItem, StatusCode


def path_helper() -> str:
    return '/home/papaggalos/workspace/python_agent_gemini/python_agent_gemini/calculator/pkg/'

# # # TODO dest has dot inside e.g. pkg/./k
# DEPRECATED TESTS -> test_get_files_info are correct 
class TestGetFilesInfo(unittest.TestCase):

    def setUp(self) -> None:
        class PathItemX:

            def __init__(self, 
                        abs_path: Path,
                        size: int, 
                        is_dir: bool):
                self.abs_path = abs_path
                self.size = size
                self.is_dir = is_dir
            
            def __eq__(self, other: object, msg) -> bool: # type: ignore

                if not isinstance(other, PathItem):
                    return NotImplemented
                
                return all([
                    self.abs_path == other.abs_path,
                    self.size == other.size,
                    self.is_dir == other.is_dir])
        
        self.addTypeEqualityFunc(typeobj=PathItem, 
                                 function=PathItemX.__eq__) # type: ignore[arg-type]

    def test_success_current_dir(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory=".")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_IS, status_code)
        self.assertEqual(('\tSuccess: "." is the working directory'), 
                         (msg))
    
    def test_not_a_direcotry(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="does_not_exist")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.NOT_A_DIR, status_code)
        self.assertEqual(('\tError: Cannot list "does_not_exist" as it is not a dir'), 
                         (msg))

    def test_error_normal(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/bin")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "/bin" as it is outside the permitted working directory'), 
                         (msg))

    def test_error_double_dot(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="../")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (msg))
    
    def test_success_nested_file(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="main.py")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.NOT_A_DIR, status_code)
        self.assertEqual(('\tError: Cannot list "main.py" as it is not a dir'), 
                         (msg))
                          
    # ///////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////
    # ///// above tests, test the error logic
    # ///// below tests, test the return values and logic !!
    # ////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////

    # This test is wrong and passes the unittest. small-test catches this 
    # is this __eq__ operator defined wrong ?      TODO
    def test_success_dot_current(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory=".")
        (_, _, msg), files = dir_info

        print(f'{msg=}')
        print(f'{files=}')

        self.assertEqual(('\tSuccess: "." is the working directory'), 
                         (msg))
        # TODO removing 'calculator/' string from here still passes !
        self.assertEqual(PathItem(abs_path=Path('calculator/'+"__init__.py"), 
                                  size=0, 
                                  is_dir=False), 
                        files[0])
        self.assertEqual(PathItem(abs_path=Path('calculator/'+"main.py"), 
                                  size=741, 
                                  is_dir=False), 
                        files[1])
        self.assertEqual(PathItem(abs_path=Path('calculator/'+"tests.py"), 
                                  size=1354, 
                                  is_dir=False), 
                        files[2])
        
    
    def test_success_nest(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg")
        (is_err, status_code, msg), files = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')
        print(f'{files=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg" is within the working directory'), 
                         (msg))

        self.assertEqual(PathItem(abs_path=Path(path_helper()+"__init__.py"), 
                        size=0, 
                        is_dir=False), files[0])
        self.assertEqual(PathItem(abs_path=Path(path_helper()+"morelorem.txt"), 
                            size=26, 
                            is_dir=False), files[1])
        self.assertEqual(PathItem(abs_path=Path(path_helper()+"render.py"), 
                            size=440, 
                            is_dir=False), files[2])   

    def test_success_nest_nest_same_name(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg/pkg")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg/pkg" is within the working directory'), 
                         (msg))

    # TODO maybe we want to apply formatting to the resulting string?
    def test_success_nest_same_name(self) -> None:

        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/calculator")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)

        # ----------------------------------------------

        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="calculator/")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')
        
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/" is within the working directory'), 
                         (msg))
        
        # ----------------------------------------------
        # TODO FIX (**4**)
        # dir_info = DirInfo(working_directory=Path("calculator/"), dest_directory="calculator")
        # (is_err, status_code, msg), _ = dir_info

        # print(f'{is_err=}')
        # print(f'{status_code=}')
        # print(f'{msg=}')

        # self.assertEqual(False, is_err)
        # self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        # self.assertEqual(('\tSuccess: "calculator" is within the working directory'), (msg))
        
        # ----------------------------------------------

        dir_info = DirInfo(working_directory=Path("calculator/"), 
                           dest_directory="calculator/calculator/")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/calculator/" is within the working directory'), 
                         (msg))
        
        # ----------------------------------------------

        dir_info = DirInfo(working_directory=Path("calculator/"), 
                           dest_directory="calculator/calculator/calculator/")
        (is_err, status_code, msg), _ = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')
        
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/calculator/calculator/" is within the working directory'), 
                         (msg))
        
    # TODO add a test to list files of deeply nested dir
    def test_success_nest_nest(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg/new")
        (is_err, status_code, msg), files = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')
        print(f'{files=}')

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg/new" is within the working directory'), 
                         (msg))

    def test_error_one(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/bin")
        (is_err, status_code, _), files = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{files=}')

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual([], files)
        
    def test_error_two(self) -> None:
        dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="../")
        (is_err, status_code, msg), files = dir_info

        print(f'{is_err=}')
        print(f'{status_code=}')
        print(f'{msg=}')
        print(f'{files=}')

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (msg))
        self.assertEqual([], files)


if __name__ == '__main__':

    unittest.main()
