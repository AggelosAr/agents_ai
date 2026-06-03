from pathlib import Path

from small_test import (ExpectedWasDifferentFromActual, Test, WillRaise,
                        must_equal)

from functions.run_python_file import _run_python_file


@Test.case
def test_python_file_runs() -> None:

    msg = _run_python_file(Path("calculator"), "main.py")

    print('-----------------')
    print(msg)
    print('-----------------')

    must_equal(
""" | 
 | -> STDOUT: Calculator App
Usage: python main.py "<expression>"
Example: python main.py "3 + 5"
""", msg)
        


@Test.case
def test_python_file_runs_with_args() -> None:

    msg = _run_python_file(Path("calculator"), "main.py", ["3 + 5"])

    print('-----------------')
    print(msg)
    print('-----------------')

    must_equal(""" | 
 | -> STDOUT: {
  "expression": "3 + 5",
  "result": 8
}
""", msg)



# interesting we are running tests inside tests here!
@Test.case
def test_python_file_runs_tests_within_tests() -> None:

    msg = _run_python_file(Path("calculator"), "test_calculator.py")

    print('-----------------')
    print(msg)
    print('-----------------')

    possibilities = {
        ''' | 
 | -> STDERR: .........
----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
''',''' | 
 | -> STDERR: .........
----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK
'''

    }

    must_equal(True, msg in possibilities)



@Test.case
def test_python_file_doesnt_run_since_it_is_outside() -> None:

    msg = _run_python_file(Path("calculator"), "../main.py")
    print(msg)
    must_equal('Cannot execute "../main.py" as it is outside', msg)



@Test.case
def test_python_file_not_found() -> None:

    msg = _run_python_file(Path("calculator"), "nonexistent.py")
    print(msg)
    must_equal('"nonexistent.py" does not exist', msg)



@Test.case
def test_file_wont_run_since_it_is_not_a_python_file() -> None:

    msg = _run_python_file(Path("calculator"), "lorem.txt")
    print(msg)
    must_equal('Error: "lorem.txt" is not a Python file', msg)
