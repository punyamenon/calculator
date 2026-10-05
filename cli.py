"""Interactive Command-Line Interface (CLI) for the Calculator."""

import sys
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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
    format_number,
    history,
)

DIVIDER = "=" * 50
SUB_DIVIDER = "-" * 50


def print_banner() -> None:
    print(DIVIDER)
    print("               PYTHON CALCULATOR                ")
    print("       All Basic & Advanced Math Operations     ")
    print(DIVIDER)


def get_float_input(prompt: str) -> Optional[float]:
    """Safely prompt the user for a numeric float/int input."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ("b", "back", "cancel"):
            return None
        try:
            val = float(user_input)
            return format_number(val)
        except ValueError:
            print("  [!] Error: Invalid number. Please enter a valid integer or decimal (or 'b' to go back).")


def run_menu_operation(choice: str) -> None:
    """Execute operation chosen from standard menu."""
    ops = {
        "1": ("Addition (+)", add, "+"),
        "2": ("Subtraction (-)", subtract, "-"),
        "3": ("Multiplication (*)", multiply, "*"),
        "4": ("Division (/)", divide, "/"),
        "5": ("Floor Division (//)", integer_divide, "//"),
        "6": ("Modulo / Remainder (%)", modulo, "%"),
        "7": ("Exponentiation / Power (^)", power, "^"),
        "8": ("Square Root (√)", square_root, "√"),
    }

    if choice not in ops:
        print("  [!] Invalid choice. Please select from the menu.")
        return

    name, func, symbol = ops[choice]
    print(f"\n--- {name} ---")

    if choice == "8":
        # Unary operation
        num = get_float_input("Enter number: ")
        if num is None:
            return
        try:
            res = func(num)
            formatted = format_number(res)
            expr = f"√{num}"
            print(f"\n  Result: {expr} = {formatted}")
            history.add(expr, formatted)
        except ValueError as e:
            print(f"\n  [!] Error: {e}")
    else:
        # Binary operation
        num1 = get_float_input("Enter first number: ")
        if num1 is None:
            return
        num2 = get_float_input("Enter second number: ")
        if num2 is None:
            return

        try:
            res = func(num1, num2)
            formatted = format_number(res)
            expr = f"{num1} {symbol} {num2}"
            print(f"\n  Result: {expr} = {formatted}")
            history.add(expr, formatted)
        except (ZeroDivisionError, OverflowError, ValueError) as e:
            print(f"\n  [!] Error: {e}")


def run_expression_mode() -> None:
    """Allow user to enter arbitrary mathematical expressions."""
    print("\n--- Expression Evaluator ---")
    print("Enter any expression (e.g. '12 + 5 * (4 - 2)', 'sqrt(64) + 2^3').")
    print("Type 'back' to return to main menu.\n")

    while True:
        try:
            expr = input("calc > ").strip()
            if not expr:
                continue
            if expr.lower() in ("b", "back", "q", "quit", "exit"):
                break

            result = evaluate_expression(expr)
            print(f"       = {result}")
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"       [!] Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print()
            break


def show_history() -> None:
    """Display calculation history."""
    entries = history.get_all()
    print("\n--- Calculation History ---")
    if not entries:
        print("  No calculations recorded yet.")
    else:
        for idx, entry in enumerate(entries, start=1):
            print(f"  {idx:2d}. {entry}")
    print(SUB_DIVIDER)


def main_cli() -> None:
    """Main CLI loop."""
    print_banner()

    while True:
        print("\nMain Menu:")
        print("  [1] Addition (+)")
        print("  [2] Subtraction (-)")
        print("  [3] Multiplication (*)")
        print("  [4] Division (/)")
        print("  [5] Floor Division (//)")
        print("  [6] Modulo (%)")
        print("  [7] Power (^)")
        print("  [8] Square Root (√)")
        print("  [E] Quick Expression Mode (e.g. 15 + 4 * 2)")
        print("  [H] View History")
        print("  [C] Clear History")
        print("  [Q] Quit")

        try:
            choice = input("\nSelect an option: ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting calculator. Goodbye!")
            sys.exit(0)

        if choice in ("1", "2", "3", "4", "5", "6", "7", "8"):
            run_menu_operation(choice)
        elif choice == "E":
            run_expression_mode()
        elif choice == "H":
            show_history()
        elif choice == "C":
            history.clear()
            print("\n  [✓] Calculation history cleared.")
        elif choice in ("Q", "QUIT", "EXIT"):
            print("\nThank you for using Python Calculator. Goodbye!")
            break
        else:
            print("  [!] Unrecognized option. Please choose from the menu.")


if __name__ == "__main__":
    main_cli()
