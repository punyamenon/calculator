# Python Calculator

A robust, full-featured Python calculator supporting all basic and advanced mathematical operations with both an **Interactive Terminal CLI** and a **Modern Desktop GUI (Tkinter)**.

---

## Features

- **All Basic & Extended Arithmetic Operations**:
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*` or `×`)
  - Division (`/` or `÷`) with safe division-by-zero handling
  - Floor Division (`//`)
  - Modulo / Remainder (`%`)
  - Exponentiation / Power (`^` or `**`)
  - Square Root (`√` or `sqrt(...)`)
  - Parentheses (`(`, `)`) with proper mathematical order of operations (PEMDAS)
- **Two User Interfaces**:
  - **Interactive Terminal CLI** (`cli.py`): Step-by-step menu, quick expression evaluation mode, and history review.
  - **Modern Desktop GUI** (`gui.py`): Clean dark-theme calculator window with click buttons, live expression preview, keyboard input support, and history popup.
- **Direct Command-Line Evaluation**: Evaluate expressions directly with `-e` (e.g. `python main.py -e "sqrt(144) + 2^4"`).
- **Safe Evaluation**: Built using Python's Abstract Syntax Tree (`ast`) parser to safely compute expressions without risky code execution (`eval`).
- **Calculation History**: Stores recent operations with timestamps and allows viewing/clearing.
- **Comprehensive Unit Tests**: 100% test coverage across all operations and edge cases.

---

## Quick Start

### 1. Launch the Calculator
```bash
python main.py
```
This presents a menu to choose between the **Terminal CLI** and **Desktop GUI**.

### 2. Launch Desktop GUI Directly
```bash
python main.py --gui
# or
python gui.py
```

### 3. Launch Terminal CLI Directly
```bash
python main.py --cli
# or
python cli.py
```

### 4. Evaluate an Expression from Terminal
```bash
python main.py -e "(15 + 25) * 3 / 2"
# Output: 60

python main.py -e "sqrt(81) + 2^5"
# Output: 41
```

---

## Project Structure

```
calculator/
├── calculator.py       # Core mathematical operations and safe AST parser
├── cli.py              # Interactive terminal CLI (menu, expression mode, history)
├── gui.py              # Modern desktop GUI built with Tkinter
├── main.py             # Unified entry point with CLI arguments
├── test_calculator.py  # Unit test suite (19 test cases)
└── README.md           # Documentation
```

---

## Running Unit Tests

Run the test suite with:
```bash
python -m unittest test_calculator.py -v
```
All 19 test cases verify:
- Addition, subtraction, multiplication, division
- Modulo, floor division, exponentiation, square root
- Division by zero and negative square root errors
- Operator precedence and parentheses
- Number formatting and calculation history
