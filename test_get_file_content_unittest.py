import unittest
from pathlib import Path

from functions.consts import MAX_CHARS, OFFSET
from functions.get_file_contents import _get_file_contents
from functions.get_files_info import StatusCode
from tests.test_utils import break_down, set_up


class TestGetFilesInfo(unittest.TestCase):

    def test_truncation_just(self) -> None:
        set_up()
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        

        self.assertEqual(False, err)

        self.assertEqual(len(contents) < MAX_CHARS + OFFSET, True) # '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
        assert 'truncated' not in contents
        print(f'lorem.txt length: {len(contents)}')

        self.assertEqual(10000, len(contents))

        break_down()



    def test_truncation_bigger(self) -> None:
        set_up(characters=111789)
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        
        self.assertEqual(False, err)
    
        self.assertEqual(len(contents) > MAX_CHARS + OFFSET, True) # '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )

        assert 'truncated' in contents
        print(f'lorem.txt length: {len(contents)}')
        #print(f'lorem.txt truncated: {'truncated' in contents}')

        self.assertEqual(10051, len(contents))
        
        break_down()



    def test_truncation_smaller(self) -> None:
        set_up(characters=8_999)
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        
        self.assertEqual(False, err)

        assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
        assert 'truncated' not in contents
        print(f'lorem.txt length: {len(contents)}')
        #print(f'lorem.txt truncated: {'truncated' in contents}')

        self.assertEqual(8999, len(contents))

        break_down()



    def test_truncation_small(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        
        self.assertEqual(False, err)

        assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
        assert 'truncated' not in contents
        print(f'main.py length: {len(contents)}')
        #print(f'main.py truncated: {'truncated' in contents}')

        self.assertEqual(742, len(contents))




    def test_simple_truncation_works_as_expected(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        
        self.assertEqual(False, err)

        assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
        assert ('truncated' in contents) is False
        assert 'expression = " ".join(sys.argv[1:])' in contents
        print(f'main.py length: {len(contents)}')

        self.assertEqual(742, len(contents))

        #print(f'main.py truncated: {'truncated' in contents}')

    # ///////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////
    # ///// Tests above test truncation
    # ///// Tests below should test behaviour
    # ////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////


    def test_fails_to_get_dir_as_it_does_not_exist(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='/bin/cat')
        
        self.assertEqual(True, err)

        assert 'Error: Cannot ' in msg  and 'permitted working' in msg
        
        print('---------------------')
        print(msg)
        print('---------------------')

        self.assertEqual('', contents)

        

    def test_gets_the_deeply_nested_file_data(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='pkg/pkg/sample.txt')

        self.assertEqual(False, err)

        self.assertEqual(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

        assert 'kappa' in contents and 'OK' in contents

        print('---------------------')
        print(contents)
        print('---------------------')




    def test_gets_the_current_dir_file_data(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        
        self.assertEqual(False, err)

        self.assertEqual(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

        assert 'if len(sys.argv) <= 1:' in contents and 'expression = " ".join(sys.argv[1:])' in contents

        print('---------------------')
        print(contents)
        print('---------------------')



    def test_fails_to_get_outside_file_data(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='/main.py')
        
        self.assertEqual(True, err)

        self.assertEqual(StatusCode.OUTSIDE.value, status.value)



    def test_fails_to_get_file_since_dir_does_not_exist(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='pkg/does_not_exist.py')
        
        print(msg)

        self.assertEqual(True, err)

        self.assertEqual(StatusCode.FILE_NOT_FOUND.value, status.value)

        self.assertEqual('\tError: File not found or is not a regular file: "does_not_exist.py"', msg)

        self.assertEqual('', contents)




    def test_failed(self) -> None:
        # Failed in getting file data in existing nested direstory but not existing file
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='calculator/calculator.py')

        self.assertEqual(True, err)

        self.assertEqual(StatusCode.FILE_NOT_FOUND.value, status.value)
        
        assert msg == '\tError: File not found or is not a regular file: "calculator.py"'

        self.assertEqual('', contents)



    def test_s_one(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        self.assertEqual(False, err)

        self.assertEqual(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

        assert 'expression = " ".join(sys.argv[1:])' in contents



    def test_s_two(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='__init__.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        self.assertEqual(False, err)

        self.assertEqual(StatusCode.SUCCESS_FILE_FOUND.value, status.value)
        
        assert 'def main() -> None:' in contents
        assert 'def _apply_operator(self, operators: list[str], values: list[float])' in contents



    def test_s_two_two(self) -> None:
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='calculator/pkg/calculator.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        self.assertEqual(False, err)

        self.assertEqual(StatusCode.SUCCESS_FILE_FOUND.value, status.value)

        assert 'def _apply_operator(self, operators' in contents



if __name__ == '__main__':
    unittest.main()
