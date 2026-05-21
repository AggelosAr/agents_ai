from functions.run_python_file import run_python_file
from tests.test_utils import discover, test_case


@discover(globals=globals())
def main():


    @test_case
    def test_python_file_runs():

        msg = run_python_file("calculator", "main.py")
        print(msg)
        assert """STDOUT: Calculator App
Usage: python main.py "<expression>"
Example: python main.py "3 + 5""" in msg
        

    @test_case
    def test_python_file_runs_with_args():

        msg = run_python_file("calculator", "main.py", ["3 + 5"])
        print(msg)
        assert """STDOUT: {
"expression": "3 + 5",
"result": 8
}""" in msg


    @test_case
    def test_python_file_runs_tests_within_tests():

        msg = run_python_file("calculator", "tests.py")
        print(msg)
        assert "STDERR: ........." in msg


    @test_case
    def test_python_file_doesnt_run_since_it_is_outside():

        msg = run_python_file("calculator", "../main.py")
        print(msg)
        assert 'Error' in msg and 'is outside the permitted working directory' in msg


    @test_case
    def test_python_file_not_found():

        msg = run_python_file("calculator", "nonexistent.py")
        print(msg)
        assert 'Error' in msg and 'File not found or is not a regular file' in msg


    @test_case
    def test_file_wont_run_since_it_is_not_a_python_file():

        msg = run_python_file("calculator", "lorem.txt")
        print(msg)
        assert 'Error' in msg and 'not a Python file' in msg


    test_python_file_runs()
    test_python_file_runs_with_args()
    test_python_file_runs_tests_within_tests()
    test_python_file_doesnt_run_since_it_is_outside()
    test_python_file_not_found()
    test_file_wont_run_since_it_is_not_a_python_file()

if __name__=='__main__':
    main()


