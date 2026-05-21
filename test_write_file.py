from pathlib import Path

from functions.write_file import write_file
from test_get_file_content import break_down, set_up
from tests.test_utils import break_down, discover, set_up, test_case

# TODO later upate tests to test the status


@discover(globals=globals())
def main():


    @test_case
    def test_successfully_overwrote_file_contents():
        set_up(characters=100)
        (err, status, msg), contents = write_file(working_directory=Path('calculator'), 
                                                  file_path='lorem.txt', 
                                                  content="wait, this isn't lorem ipsum")
        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{contents=}')
        assert 'Successfully wrote to' in msg and 'haracters wr' in msg and '28' in msg
        assert "wait, this isn't lorem ipsum" in contents
        break_down()


    @test_case
    def test_successfully_wrote_to_file_when_file_did_not_exist(): 
        (err, status, msg), contents = write_file(working_directory=Path('calculator'), 
                                                  file_path='lorem.txt', 
                                                  content="wait, this isn't lorem ipsum")
        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{contents=}')
        assert 'Successfully wrote to' in msg and 'haracters wr' in msg
        assert "wait, this isn't lorem ipsum" in contents
        break_down()


    @test_case
    def test_successfully_wrote_to_nested_dir():
        (err, status, msg), contents = write_file(working_directory=Path('calculator'), 
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


    @test_case
    def test_successfully_overwrote_to_nested_dir():
        set_up(characters=100, dest='pkg/morelorem.txt')
        (err, status, msg), contents = write_file(working_directory=Path('calculator'), 
                                                  file_path='pkg/morelorem.txt', 
                                                  content='lorem ipsum dolor sit ')
        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{contents=}')
        assert 'Successfully wrote to' in msg
        assert 'lorem ipsum dolor sit ' in contents
        break_down(dest='pkg/morelorem.txt')


    @test_case
    def test_illegal_action():
        (err, status, msg), contents = write_file(working_directory=Path('calculator'), 
                                                  file_path='/tmp/temp.txt', 
                                                  content='this should not be allowed')
        print(f'{err=}')
        print(f'{status=}')
        print(f'{msg=}')
        print(f'{contents=}')
        assert err is True
        assert '\tError: Cannot list "/tmp/temp.txt" as it is outside the permitted working directory' == msg
        assert contents is None

    test_successfully_overwrote_file_contents()
    test_successfully_wrote_to_file_when_file_did_not_exist()
    test_successfully_wrote_to_nested_dir()
    test_successfully_overwrote_to_nested_dir()
    test_illegal_action()


if __name__=='__main__':
    main()    
