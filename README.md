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
- **Three User Interfaces**:
  - **Modern Web App (Streamlit)** (`streamlit_app.py` / `app.py`): Beautiful browser interface with OLED-style digital display, clickable keypad, direct formula input, unit converter, number theory tools, and session history.
  - **Interactive Terminal CLI** (`cli.py`): Step-by-step menu, quick expression evaluation mode, and history review.
  - **Modern Desktop GUI** (`gui.py`): Clean dark-theme calculator window with click buttons, live expression preview, keyboard input support, and history popup.
- **Direct Command-Line Evaluation**: Evaluate expressions directly with `-e` (e.g. `python main.py -e "sqrt(144) + 2^4"`).
- **Safe Evaluation**: Built using Python's Abstract Syntax Tree (`ast`) parser to safely compute expressions without risky code execution (`eval`).
- **Calculation History**: Stores recent operations with timestamps and allows viewing/clearing.
- **Comprehensive Unit Tests**: 100% test coverage across all operations and edge cases.
- **Streamlit Cloud Deployment**: Ready-to-deploy on [share.streamlit.io](https://share.streamlit.io) with zero configuration.

---

## Quick Start

### 1. Launch the Calculator Menu
```bash
python main.py
```
This presents an interactive menu to choose between **CLI**, **Desktop GUI**, or **Streamlit Web App**.

### 2. Launch Streamlit Web App Directly
```bash
streamlit run streamlit_app.py
# or
python main.py --web
```
Opens in your browser at `http://localhost:8501`.

### 3. Launch Desktop GUI Directly
```bash
python main.py --gui
# or
python gui.py
```

### 4. Launch Terminal CLI Directly
```bash
python main.py --cli
# or
python cli.py
```

### 5. Evaluate an Expression from Terminal
```bash
python main.py -e "(15 + 25) * 3 / 2"
# Output: 60

python main.py -e "sqrt(81) + 2^5"
# Output: 41
```

---

## Deploy to Streamlit Cloud (Hosting)

To host this calculator live on the internet for free via Streamlit Community Cloud:

1. Push your repository to GitHub: `https://github.com/<your-username>/calculator`
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
3. Click **"New app"**.
4. Set:
   - **Repository**: `<your-username>/calculator`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py` (or `app.py`)
5. Click **"Deploy!"**. Streamlit will automatically read `requirements.txt` and provide a public URL.

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
