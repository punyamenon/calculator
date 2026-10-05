"""Unit tests for the calculator module."""

import unittest
from calculator import (
    add,
    subtract,
    multiply,
    divide,
    integer_divide,
    modulo,
    power,
    square_root,
    evaluate_expression,
    CalculationHistory,
    format_number,
)


class TestBasicOperations(unittest.TestCase):
    """Test individual arithmetic functions."""

    def test_addition(self):
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(add(-3, 8), 5)
        self.assertEqual(add(-4, -6), -10)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)

    def test_subtraction(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(4, 10), -6)
        self.assertEqual(subtract(-5, -5), 0)
        self.assertAlmostEqual(subtract(5.5, 2.2), 3.3, places=7)

    def test_multiplication(self):
        self.assertEqual(multiply(6, 7), 42)
        self.assertEqual(multiply(-3, 4), -12)
        self.assertEqual(multiply(-5, -5), 25)
        self.assertEqual(multiply(100, 0), 0)
        self.assertAlmostEqual(multiply(2.5, 4), 10.0)

    def test_division(self):
        self.assertEqual(divide(20, 4), 5.0)
        self.assertAlmostEqual(divide(10, 3), 3.3333333333, places=5)
        self.assertEqual(divide(-12, 3), -4.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_integer_divide(self):
        self.assertEqual(integer_divide(17, 5), 3)
        self.assertEqual(integer_divide(-17, 5), -4)
        with self.assertRaises(ZeroDivisionError):
            integer_divide(10, 0)

    def test_modulo(self):
        self.assertEqual(modulo(17, 5), 2)
        self.assertEqual(modulo(10, 2), 0)
        with self.assertRaises(ZeroDivisionError):
            modulo(10, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(4, 0.5), 2.0)

    def test_square_root(self):
        self.assertEqual(square_root(16), 4)
        self.assertEqual(square_root(0), 0)
        self.assertAlmostEqual(square_root(2), 1.41421356, places=5)
        with self.assertRaises(ValueError):
            square_root(-9)

    def test_format_number(self):
        self.assertEqual(format_number(5.0), 5)
        self.assertEqual(format_number(5.25), 5.25)
        self.assertEqual(format_number(7), 7)


class TestExpressionEvaluation(unittest.TestCase):
    """Test AST-based expression evaluator."""

    def test_simple_expressions(self):
        self.assertEqual(evaluate_expression("2 + 3"), 5)
        self.assertEqual(evaluate_expression("10 - 4"), 6)
        self.assertEqual(evaluate_expression("6 * 7"), 42)
        self.assertEqual(evaluate_expression("10 / 2"), 5)

    def test_precedence_and_parentheses(self):
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)
        self.assertEqual(evaluate_expression("2 ^ 3 + 1"), 9)
        self.assertEqual(evaluate_expression("2 ** 3"), 8)

    def test_alternate_symbols(self):
        self.assertEqual(evaluate_expression("6 × 7"), 42)
        self.assertEqual(evaluate_expression("20 ÷ 4"), 5)

    def test_sqrt_function(self):
        self.assertEqual(evaluate_expression("sqrt(25) + 3"), 8)

    def test_floor_div_and_modulo(self):
        self.assertEqual(evaluate_expression("19 // 4"), 4)
        self.assertEqual(evaluate_expression("19 % 4"), 3)

    def test_unary_operators(self):
        self.assertEqual(evaluate_expression("-5 + 12"), 7)
        self.assertEqual(evaluate_expression("+10 - -5"), 15)

    def test_invalid_syntax_and_operators(self):
        with self.assertRaises(ValueError):
            evaluate_expression("2 ++")
        with self.assertRaises(ValueError):
            evaluate_expression("")
        with self.assertRaises(ZeroDivisionError):
            evaluate_expression("10 / 0")

    def test_security_prevents_arbitrary_code(self):
        with self.assertRaises(ValueError):
            evaluate_expression("__import__('os').system('dir')")


class TestCalculationHistory(unittest.TestCase):
    """Test history tracker."""

    def test_history_records(self):
        hist = CalculationHistory(max_entries=3)
        hist.add("1 + 1", 2)
        hist.add("2 + 2", 4)
        self.assertEqual(len(hist.get_all()), 2)
        hist.add("3 + 3", 6)
        hist.add("4 + 4", 8)
        self.assertEqual(len(hist.get_all()), 3)
        self.assertEqual(hist.get_all()[-1].result, "8")
        hist.clear()
        self.assertEqual(len(hist.get_all()), 0)


if __name__ == "__main__":
    unittest.main()
