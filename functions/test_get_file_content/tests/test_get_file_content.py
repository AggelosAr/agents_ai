from pathlib import Path

from small_test import Test, must_equal

from functions.consts import MAX_CHARS, OFFSET
from functions.get_file_contents import _get_file_contents
from functions.get_files_info import StatusCode
from tests.test_utils import break_down, set_up

# TODO assert exceptions is woring as intended
# TODO test file object 

    
@Test.case
def test_truncation_just() -> None:
    set_up()
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='lorem.txt')
    

    must_equal(False, err)

    must_equal(len(contents) < MAX_CHARS + OFFSET, True) # '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
    assert 'truncated' not in contents
    print(f'lorem.txt length: {len(contents)}')

    must_equal(10000, len(contents))

    break_down()


@Test.case
def test_truncation_bigger() -> None:
    set_up(characters=111789)
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='lorem.txt')
    
    must_equal(False, err)
 
    must_equal(len(contents) > MAX_CHARS + OFFSET, True) # '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )

    assert 'truncated' in contents
    print(f'lorem.txt length: {len(contents)}')
    #print(f'lorem.txt truncated: {'truncated' in contents}')

    must_equal(10051, len(contents))
    
    break_down()


@Test.case
def test_truncation_smaller() -> None:
    set_up(characters=8_999)
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='lorem.txt')
    
    must_equal(False, err)

    assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
    assert 'truncated' not in contents
    print(f'lorem.txt length: {len(contents)}')
    #print(f'lorem.txt truncated: {'truncated' in contents}')

    must_equal(8999, len(contents))

    break_down()


@Test.case
def truncation_small() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='main.py')
    
    must_equal(False, err)

    assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
    assert 'truncated' not in contents
    print(f'main.py length: {len(contents)}')
    #print(f'main.py truncated: {'truncated' in contents}')

    must_equal(742, len(contents))



@Test.case
def simple_truncation_works_as_expected() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='main.py')
    
    must_equal(False, err)

    assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
    assert ('truncated' in contents) is False
    assert 'expression = " ".join(sys.argv[1:])' in contents
    print(f'main.py length: {len(contents)}')

    must_equal(742, len(contents))

    #print(f'main.py truncated: {'truncated' in contents}')

# ///////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////
# ///// Tests above test truncation
# ///// Tests below should test behaviour
# ////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////

@Test.case
def fails_to_get_dir_as_it_does_not_exist() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='/bin/cat')
    
    must_equal(True, err)

    assert 'Error: Cannot ' in msg  and 'permitted working' in msg
    
    print('---------------------')
    print(msg)
    print('---------------------')

    must_equal(None, contents)

    
@Test.case
def gets_the_deeply_nested_file_data() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='pkg/pkg/sample.txt')

    must_equal(False, err)

    must_equal(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

    assert 'kappa' in contents and 'OK' in contents

    print('---------------------')
    print(contents)
    print('---------------------')



@Test.case
def gets_the_current_dir_file_data() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='main.py')
    
    must_equal(False, err)

    must_equal(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

    assert 'if len(sys.argv) <= 1:' in contents and 'expression = " ".join(sys.argv[1:])' in contents

    print('---------------------')
    print(contents)
    print('---------------------')


@Test.case
def test_fails_to_get_outside_file_data() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='/main.py')
    
    must_equal(True, err)

    must_equal(StatusCode.OUTSIDE.value, status.value)


@Test.case
def fails_to_get_file_since_dir_does_not_exist() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='pkg/does_not_exist.py')
    
    print(msg)

    must_equal(True, err)

    must_equal(StatusCode.FILE_NOT_FOUND.value, status.value)

    must_equal('\tError: File not found or is not a regular file: "does_not_exist.py"', msg)

    must_equal(None, contents)



@Test.case
def failed() -> None:
    # Failed in getting file data in existing nested direstory but not existing file
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='calculator/calculator.py')

    must_equal(True, err)

    must_equal(StatusCode.FILE_NOT_FOUND.value, status.value)
    
    assert msg == '\tError: File not found or is not a regular file: "calculator.py"'

    must_equal(None, contents)


@Test.case
def s_one() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='main.py')

    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{file=}')
    print(f'{contents=}')

    must_equal(False, err)

    must_equal(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

    assert 'expression = " ".join(sys.argv[1:])' in contents


@Test.case
def s_two() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='__init__.py')

    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{file=}')
    print(f'{contents=}')

    must_equal(False, err)

    must_equal(StatusCode.SUCCESS_FILE_FOUND.value, status.value)
    
    assert 'def main() -> None:' in contents
    assert 'def _apply_operator(self, operators: list[str], values: list[float])' in contents


@Test.case
def s_two() -> None:
    (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                file_path='calculator/pkg/calculator.py')

    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{file=}')
    print(f'{contents=}')

    must_equal(False, err)

    must_equal(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

    assert 'def _apply_operator(self, operators' in contents
