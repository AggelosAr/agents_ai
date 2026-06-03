from pathlib import Path

from small_test import Test, must_equal

from functions.get_files_info import DirInfo, PathItem, StatusCode

# # # TODO test has dot inside e.g. pkg/./k


def path_helper() -> str:
    return '/home/papaggalos/workspace/python_agent_gemini/python_agent_gemini/calculator/pkg/'


@Test.case
def test_success_current_dir() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory=".")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_IS, status_code)
    must_equal(('\tSuccess: "." is the working directory'), (msg))


@Test.case
def test_not_a_direcotry() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="does_not_exist")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(False, is_err)
    must_equal(StatusCode.NOT_A_DIR, status_code)
    must_equal(('\tError: Cannot list "does_not_exist" as it is not a dir'), (msg))


@Test.case
def test_error_normal() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/bin")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(True, is_err)
    must_equal(StatusCode.OUTSIDE, status_code)
    must_equal(('\tError: Cannot list "/bin" as it is outside the permitted working directory'), (msg))


@Test.case
def test_error_double_dot() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="../")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(True, is_err)
    must_equal(StatusCode.OUTSIDE, status_code)
    must_equal(('\tError: Cannot list "../" as it is outside the permitted working directory'), (msg))


@Test.case
def test_success_nested_file() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="main.py")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(False, is_err)
    must_equal(StatusCode.NOT_A_DIR, status_code)
    must_equal(('\tError: Cannot list "main.py" as it is not a dir'), (msg))
                        
# ///////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////
# ///// above tests, test the error logic
# ///// below tests, test the return values and logic !!
# ////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////

@Test.case
def test_success_dot_current() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory=".")
    (_, _, msg), files = dir_info

    print(f'{msg=}')
    print(f'{files=}')

    must_equal(('\tSuccess: "." is the working directory'), (msg))

    must_equal(PathItem(abs_path=Path('calculator/'+"__init__.py"), 
                        size=95, 
                        is_dir=False), files[0])
    must_equal(PathItem(abs_path=Path('calculator/'+"main.py"), 
                        size=742, 
                        is_dir=False), files[1])
    must_equal(PathItem(abs_path=Path('calculator/'+"test_calculator.py"), 
                        size=1415, 
                        is_dir=False), files[2])
 

@Test.case
def test_success_nest() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg")
    (is_err, status_code, msg), files = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')
    print(f'{files=}')

    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)  

    must_equal(('\tSuccess: "pkg" is within the working directory'), 
                (msg))


    must_equal(PathItem(abs_path=Path(path_helper()+"__init__.py"), 
                        size=0, 
                        is_dir=False), files[0])
    must_equal(PathItem(abs_path=Path(path_helper()+"morelorem.txt"), 
                        size=26, 
                        is_dir=False), files[1])
    must_equal(PathItem(abs_path=Path(path_helper()+"render.py"), 
                        size=440, 
                        is_dir=False), files[2])   


@Test.case
def test_success_nest_nest_same_name() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg/pkg")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')

    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    must_equal(('\tSuccess: "pkg/pkg" is within the working directory'), (msg))


# TODO maybe we want to apply formatting to the resulting string?
@Test.case
def test_success_nest_same_name() -> None:

    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/calculator")
    (is_err, status_code, msg), _ = dir_info

    print('------------------------------')
    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')
    print('------------------------------')
    must_equal(True, is_err)
    must_equal(StatusCode.OUTSIDE, status_code)

    # ----------------------------------------------

    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="calculator/")
    (is_err, status_code, msg), _ = dir_info
    print('------------------------------')
    print(f'{is_err=}')
    print()
    print(f'{status_code=}')
    print()
    print(f'{msg=}')
    print('------------------------------')
    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    must_equal(('\tSuccess: "calculator/" is within the working directory'), (msg))
    
    # ----------------------------------------------
    # TODO FIX (**4**)
    # dir_info = DirInfo(working_directory=Path("calculator/"), dest_directory="calculator")
    # (is_err, status_code, msg), _ = dir_info
    # print('------------------------------')
    # print(f'{is_err=}')
    # print()    
    # print(f'{status_code=}')
    # print()
    # print(f'{msg=}')
    # print('------------------------------')
    # must_equal(False, is_err)
    # must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    # must_equal(('\tSuccess: "calculator" is within the working directory'), (msg))
    
    # ----------------------------------------------

    dir_info = DirInfo(working_directory=Path("calculator/"), 
                       dest_directory="calculator/calculator/")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')
    print()
    print(f'{status_code=}')
    print()
    print(f'{msg=}')

    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    must_equal(('\tSuccess: "calculator/calculator/" is within the working directory'), (msg))
    
    # ----------------------------------------------

    dir_info = DirInfo(working_directory=Path("calculator/"), 
                       dest_directory="calculator/calculator/calculator/")
    (is_err, status_code, msg), _ = dir_info

    print(f'{is_err=}')

    print(f'{status_code=}')
    print(f'{msg=}')
    
    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    must_equal(('\tSuccess: "calculator/calculator/calculator/" is within the working directory'), (msg))
    

# TODO add a test to list files of deeply nested dir
@Test.case
def test_success_nest_nest() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="pkg/new")
    (is_err, status_code, msg), files = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')
    print(f'{files=}')

    must_equal(False, is_err)
    must_equal(StatusCode.SUCCESS_DIR_WITHIN, status_code)
    must_equal(('\tSuccess: "pkg/new" is within the working directory'), (msg))


@Test.case
def test_error_one() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="/bin")
    (is_err, status_code, _), files = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{files=}')

    must_equal(True, is_err)
    must_equal(StatusCode.OUTSIDE, status_code)
    must_equal([], files)
    
    
@Test.case
def test_error_two() -> None:
    dir_info = DirInfo(working_directory=Path("calculator"), dest_directory="../")
    (is_err, status_code, msg), files = dir_info

    print(f'{is_err=}')
    print(f'{status_code=}')
    print(f'{msg=}')
    print(f'{files=}')

    must_equal(True, is_err)
    must_equal(StatusCode.OUTSIDE, status_code)
    must_equal(('\tError: Cannot list "../" as it is outside the permitted working directory'), (msg))
    must_equal([], files)

