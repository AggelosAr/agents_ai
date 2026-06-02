import unittest
from pathlib import Path

from functions.run_python_file import _run_python_file


class TestGetFilesInfo(unittest.TestCase):


    def test_python_file_runs(self) -> None:

        msg = _run_python_file(Path("calculator"), "main.py")

        print('-----------------')
        print(msg)
        print('-----------------')

        self.assertEqual(
""" | 
 | -> STDOUT: Calculator App
Usage: python main.py "<expression>"
Example: python main.py "3 + 5"
""", msg)
            

    def test_python_file_runs_with_args(self) -> None:

        msg = _run_python_file(Path("calculator"), "main.py", ["3 + 5"])

        print('-----------------')
        print(msg)
        print('-----------------')

        self.assertEqual(""" | 
 | -> STDOUT: {
  "expression": "3 + 5",
  "result": 8
}
""", msg)


    # interesting we are running tests inside tests here!

    def test_python_file_runs_tests_within_tests(self) -> None:

        msg = _run_python_file(Path("calculator"), "tests.py")

        print('-----------------')
        print(msg)
        print('-----------------')

        self.assertEqual(''' | 
 | -> STDERR: .........
----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
''', msg)


    def test_python_file_doesnt_run_since_it_is_outside(self) -> None:

        msg = _run_python_file(Path("calculator"), "../main.py")
        print(msg)
        self.assertEqual('Cannot execute "../main.py" as it is outside', msg)


    def test_python_file_not_found(self) -> None:

        msg = _run_python_file(Path("calculator"), "nonexistent.py")
        print(msg)
        self.assertEqual('"nonexistent.py" does not exist', msg)


    def test_file_wont_run_since_it_is_not_a_python_file(self) -> None:

        msg = _run_python_file(Path("calculator"), "lorem.txt")
        print(msg)
        self.assertEqual('Error: "lorem.txt" is not a Python file', msg)



if __name__ == '__main__':
    unittest.main()
