#calculator/tests.py
# Make unittest to ignore this path ...

from small_test import Test, WillRaise, must_equal

from ..pkg.calculator import Calculator

calculator = Calculator()

@Test.case
def test_addition():
    result = calculator.evaluate("3 + 5")
    must_equal(result, 8.0)

@Test.case
def test_subtraction():
    result = calculator.evaluate("10 - 4")
    must_equal(result, 6.0)

@Test.case
def test_multiplication():
    result = calculator.evaluate("3 * 4")
    must_equal(result, 12.0)

@Test.case
def test_division():
    result = calculator.evaluate("10 / 2")
    must_equal(result, 5.0)

@Test.case
def test_nested_expression():
    result = calculator.evaluate("3 * 4 + 5")
    must_equal(result, 17.0)

@Test.case
def test_complex_expression():
    result = calculator.evaluate("2 * 3 - 8 / 2 + 5")
    must_equal(result, 7.0)

@Test.case
def test_empty_expression():
    result = calculator.evaluate("")
    must_equal(result, None)

@Test.case
def test_invalid_operator():
    with WillRaise(ValueError):
        calculator.evaluate("$ 3 5")

@Test.case
def test_not_enough_operands():
    with WillRaise(ValueError):
        calculator.evaluate("+ 3")
