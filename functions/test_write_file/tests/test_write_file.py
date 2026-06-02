from pathlib import Path

from small_test import Test, must_equal

from functions.test_get_file_content.tests.test_get_file_content import (
    break_down, set_up)
from functions.write_file import _write_file
from tests.test_utils import break_down, set_up

# TODO later update tests to test the status



@Test.case
def test_successfully_overwrote_file_contents() -> None:
    set_up(characters=100)
    (err, status, msg), contents = _write_file(working_directory=Path('calculator'), 
                                                file_path='lorem.txt', 
                                                content="wait, this isn't lorem ipsum")
    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{contents=}')
    assert 'Successfully wrote to' in msg and 'haracters wr' in msg and '28' in msg
    assert "wait, this isn't lorem ipsum" in contents


    break_down()


@Test.case
def test_successfully_wrote_to_file_when_file_did_not_exist() -> None: 
    (err, status, msg), contents = _write_file(working_directory=Path('calculator'), 
                                                file_path='lorem.txt', 
                                                content="wait, this isn't lorem ipsum")
    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{contents=}')
    assert 'Successfully wrote to' in msg and 'haracters wr' in msg
    assert "wait, this isn't lorem ipsum" in contents
    break_down()


@Test.case
def test_successfully_wrote_to_nested_dir() -> None:
    (err, status, msg), contents = _write_file(working_directory=Path('calculator'), 
                                                file_path='pkg/morelorem.txt', 
                                                content='lorem ipsum dolor sit quat')
    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{contents=}')
    
    assert '26' in msg
    assert 'Successfully wrote to' in msg
    assert 'lorem ipsum dolor sit quat' in contents
    break_down(dest='pkg/morelorem.txt')


@Test.case
def test_successfully_overwrote_to_nested_dir() -> None:
    set_up(characters=100, dest='pkg/morelorem.txt')
    (err, status, msg), contents = _write_file(working_directory=Path('calculator'), 
                                                file_path='pkg/morelorem.txt', 
                                                content='lorem ipsum dolor sit ')
    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{contents=}')
    assert 'Successfully wrote to' in msg
    assert 'lorem ipsum dolor sit ' in contents
    break_down(dest='pkg/morelorem.txt')


@Test.case
def test_illegal_action() -> None:
    (err, status, msg), contents = _write_file(working_directory=Path('calculator'), 
                                                file_path='/tmp/temp.txt', 
                                                content='this should not be allowed')
    print(f'{err=}')
    print(f'{status=}')
    print(f'{msg=}')
    print(f'{contents=}')
    assert err is True
    assert '\tError: Cannot list "/tmp/temp.txt" as it is outside the permitted working directory' == msg
    assert contents is None
