"""Core calculator module providing basic arithmetic operations and safe expression evaluation."""

import ast
import math
import operator
from datetime import datetime
from typing import Any, List, Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of a and b."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of a and b."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def integer_divide(a: Number, b: Number) -> int:
    """Return the integer floor division of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return int(a // b)


def modulo(a: Number, b: Number) -> Number:
    """Return the remainder of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot calculate modulo by zero.")
    return a % b


def power(a: Number, b: Number) -> Number:
    """Return a raised to the power of b."""
    try:
        res = a ** b
        if isinstance(res, complex):
            raise ValueError("Result is a complex number.")
        return res
    except OverflowError:
        raise OverflowError("Calculation result is too large.")


def square_root(a: Number) -> float:
    """Return the square root of a.

    Raises:
        ValueError: If a is negative.
    """
    if a < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return math.isqrt(a) if isinstance(a, int) and math.isqrt(a) ** 2 == a else math.sqrt(a)


def format_number(val: Number) -> Number:
    """Format float with integer value into an int (e.g. 5.0 -> 5)."""
    if isinstance(val, float) and val.is_integer():
        return int(val)
    if isinstance(val, float):
        return round(val, 10)
    return val


class HistoryEntry:
    """Represents a single calculation record."""

    def __init__(self, expression: str, result: str):
        self.timestamp = datetime.now()
        self.expression = expression
        self.result = result

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {self.expression} = {self.result}"


class CalculationHistory:
    """Manages history of calculations."""

    def __init__(self, max_entries: int = 100):
        self._entries: List[HistoryEntry] = []
        self._max_entries = max_entries

    def add(self, expression: str, result: Any) -> None:
        """Add an entry to history."""
        self._entries.append(HistoryEntry(expression, str(format_number(result) if isinstance(result, (int, float)) else result)))
        if len(self._entries) > self._max_entries:
            self._entries.pop(0)

    def get_all(self) -> List[HistoryEntry]:
        """Return all history entries."""
        return list(self._entries)

    def clear(self) -> None:
        """Clear all history entries."""
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)


# Global history instance
history = CalculationHistory()


# Allowed binary operators for safe AST evaluation
_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: divide,
    ast.FloorDiv: integer_divide,
    ast.Mod: modulo,
    ast.Pow: power,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_ast_node(node: ast.AST) -> Number:
    """Safely evaluate an AST expression node."""
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Invalid constant: {node.value}")

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            operand = _eval_ast_node(node.operand)
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _BINARY_OPS:
            left = _eval_ast_node(node.left)
            right = _eval_ast_node(node.right)
            return _BINARY_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.Call):
        # Support sqrt(...)
        if isinstance(node.func, ast.Name) and node.func.id.lower() in ("sqrt", "root"):
            if len(node.args) != 1:
                raise ValueError("sqrt() takes exactly one argument.")
            arg = _eval_ast_node(node.args[0])
            return square_root(arg)
        raise ValueError(f"Unsupported function call: {ast.dump(node)}")

    raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")


def evaluate_expression(expr: str) -> Number:
    """Safely evaluate a mathematical expression string.

    Supports:
        Operators: +, -, *, /, //, %, ^ (or **), parentheses ()
        Functions: sqrt(x)
        Numbers: integers, floats, scientific notation

    Example:
        evaluate_expression("15 + 4 * 2 - sqrt(16)") -> 19
    """
    if not expr or not expr.strip():
        raise ValueError("Expression is empty.")

    cleaned = expr.strip()
    # Normalize common symbols
    cleaned = cleaned.replace("×", "*").replace("÷", "/")
    # Replace ^ with ** for exponentiation in python syntax
    cleaned = cleaned.replace("^", "**")

    try:
        parsed = ast.parse(cleaned, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e.msg}")

    result = _eval_ast_node(parsed)
    formatted = format_number(result)
    history.add(expr, formatted)
    return formatted


if __name__ == "__main__":
    from main import main
    main()

