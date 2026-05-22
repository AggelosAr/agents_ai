from pathlib import Path

from functions.consts import MAX_CHARS, OFFSET
from functions.get_file_contents import _get_file_contents
from functions.get_files_info import StatusCode
from tests.test_utils import break_down, discover, set_up, test_case

# TODO assert exceptions is woring as intended
# TODO test file object 


@discover(globals=globals())
def main():

    
    @test_case
    def test_truncation_just():
        set_up()
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        assert err is False
        assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
        assert 'truncated' not in contents
        print(f'lorem.txt length: {len(contents)}')
        #print(f'lorem.txt truncated: {'truncated' in contents}')
        break_down()


    @test_case
    def test_truncation_bigger():
        set_up(characters=111789)
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        assert err is False
        assert len(contents) > MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
        assert 'truncated' in contents
        print(f'lorem.txt length: {len(contents)}')
        #print(f'lorem.txt truncated: {'truncated' in contents}')
        break_down()


    @test_case
    def test_truncation_smaller():
        set_up(characters=8_999)
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='lorem.txt')
        assert err is False
        assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET, )
        assert 'truncated' not in contents
        print(f'lorem.txt length: {len(contents)}')
        #print(f'lorem.txt truncated: {'truncated' in contents}')
        break_down()


    @test_case
    def truncation_small():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        assert err is False
        assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
        assert 'truncated' not in contents
        print(f'main.py length: {len(contents)}')
        #print(f'main.py truncated: {'truncated' in contents}')


    @test_case
    def simple_truncation_works_as_expected():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        assert err is False
        assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET, )
        assert ('truncated' in contents) is False
        assert 'expression = " ".join(sys.argv[1:])' in contents
        print(f'main.py length: {len(contents)}')
        #print(f'main.py truncated: {'truncated' in contents}')

    # ///////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////
    # ///// Tests above test truncation
    # ///// Tests below should test behaviour
    # ////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////
    @test_case
    def fails_to_get_dir_as_it_does_not_exist():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='/bin/cat')
        assert err is True
        assert 'Error: Cannot ' in msg  and 'permitted working' in msg
        assert contents is None
        
        
    @test_case
    def gets_the_deeply_nested_file_data():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='pkg/pkg/sample.txt')

        assert err is False
        assert status == StatusCode.SUCCESS_FILE_FOUND
        assert  'kappa' in contents and 'OK' in contents


    @test_case
    def gets_the_current_dir_file_data():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='main.py')
        assert err is False
        assert status == StatusCode.SUCCESS_FILE_FOUND
        assert  'if len(sys.argv) <= 1:' in contents and 'expression = " ".join(sys.argv[1:])' in contents


    @test_case
    def test_fails_to_get_outside_file_data():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                    file_path='/main.py')
        assert err is True
        assert status == StatusCode.OUTSIDE


    @test_case
    def fails_to_get_file_since_dir_does_not_exist():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                   file_path='pkg/does_not_exist.py')
        
        print(msg)

        assert err is True
        assert status == StatusCode.FILE_NOT_FOUND
        assert '\tError: File not found or is not a regular file: "does_not_exist.py"' == msg
        assert contents is None


    @test_case
    def failed():
        # Failed in getting file data in existing nested direstory but not existing file
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                   file_path='calculator/calculator.py')

        assert err is True
        assert status == StatusCode.FILE_NOT_FOUND
        assert msg == '\tError: File not found or is not a regular file: "calculator.py"'
        assert contents is None


    @test_case
    def s_one():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                   file_path='main.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        assert err is False
        assert status == StatusCode.SUCCESS_FILE_FOUND
        assert 'expression = " ".join(sys.argv[1:])' in contents


    @test_case
    def s_two():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                   file_path='__init__.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        assert err is False
        assert status == StatusCode.SUCCESS_FILE_FOUND
        assert 'def main() -> None:' in contents
        assert 'def _apply_operator(self, operators: list[str], values: list[float])' in contents


    @test_case
    def s_two():
        (err, status, msg), (file, contents, ) = _get_file_contents(working_directory=Path('calculator'), 
                                                                   file_path='calculator/pkg/calculator.py')

        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{file=}')
        print(f'{contents=}')

        assert err is False
        assert status == StatusCode.SUCCESS_FILE_FOUND
        assert 'def _apply_operator(self, operators' in contents



    test_truncation_just()
    test_truncation_bigger()
    test_truncation_smaller()
    truncation_small()
    simple_truncation_works_as_expected()
    fails_to_get_dir_as_it_does_not_exist()
    gets_the_deeply_nested_file_data()
    gets_the_current_dir_file_data()
    test_fails_to_get_outside_file_data()
    fails_to_get_file_since_dir_does_not_exist()
    failed()
    s_one()
    s_two()


if __name__=='__main__':
    main()
