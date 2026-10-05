"""Desktop Graphical User Interface (GUI) for the Calculator using Tkinter."""

import tkinter as tk
from tkinter import font, messagebox, ttk
from typing import Optional

from calculator import (
    evaluate_expression,
    format_number,
    history,
)

# Theme Palette (Modern Dark Theme)
BG_MAIN = "#1e1e2e"
BG_DISPLAY = "#181825"
BG_BTN_NUM = "#313244"
BG_BTN_NUM_HOVER = "#45475a"
BG_BTN_OP = "#45475a"
BG_BTN_OP_HOVER = "#585b70"
BG_BTN_ACCENT = "#89b4fa"
BG_BTN_ACCENT_HOVER = "#b4befe"
BG_BTN_CLEAR = "#f38ba8"
BG_BTN_CLEAR_HOVER = "#eba0ac"
BG_BTN_EQUAL = "#a6e3a1"
BG_BTN_EQUAL_HOVER = "#94e2d5"

TEXT_LIGHT = "#cdd6f4"
TEXT_MUTED = "#9399b2"
TEXT_DARK = "#11111b"


class ModernButton(tk.Button):
    """Custom styled button with hover effects."""

    def __init__(self, master, hover_bg=None, normal_bg=None, **kwargs):
        super().__init__(master, **kwargs)
        self.normal_bg = normal_bg or kwargs.get("bg", BG_BTN_NUM)
        self.hover_bg = hover_bg or BG_BTN_NUM_HOVER
        self.configure(
            relief=tk.FLAT,
            bd=0,
            activebackground=self.hover_bg,
            cursor="hand2",
            padx=10,
            pady=10,
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self.configure(bg=self.hover_bg)

    def on_leave(self, _):
        self.configure(bg=self.normal_bg)


class CalculatorApp:
    """Main Calculator GUI Application."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("380x560")
        self.root.minsize(340, 500)
        self.root.configure(bg=BG_MAIN)

        self.current_expr = ""
        self.just_evaluated = False

        self._setup_ui()
        self._bind_keys()

    def _setup_ui(self):
        # Configure fonts
        display_font = font.Font(family="Segoe UI", size=26, weight="bold")
        sub_font = font.Font(family="Segoe UI", size=13)
        btn_font = font.Font(family="Segoe UI", size=15, weight="bold")
        icon_font = font.Font(family="Segoe UI", size=12)

        # Header bar with title and History button
        header_frame = tk.Frame(self.root, bg=BG_MAIN)
        header_frame.pack(fill=tk.X, padx=16, pady=(12, 4))

        title_lbl = tk.Label(
            header_frame,
            text="Calculator",
            font=font.Font(family="Segoe UI", size=14, weight="bold"),
            bg=BG_MAIN,
            fg=TEXT_LIGHT,
        )
        title_lbl.pack(side=tk.LEFT)

        hist_btn = tk.Button(
            header_frame,
            text="📜 History",
            font=icon_font,
            bg=BG_BTN_NUM,
            fg=TEXT_LIGHT,
            activebackground=BG_BTN_NUM_HOVER,
            activeforeground=TEXT_LIGHT,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=8,
            pady=4,
            command=self.show_history_window,
        )
        hist_btn.pack(side=tk.RIGHT)

        # Display Frame
        display_frame = tk.Frame(self.root, bg=BG_DISPLAY, bd=0, highlightthickness=1, highlightbackground="#313244")
        display_frame.pack(fill=tk.X, padx=16, pady=(8, 14))

        # Secondary expression preview (shows previous math or formula)
        self.preview_label = tk.Label(
            display_frame,
            text="",
            font=sub_font,
            bg=BG_DISPLAY,
            fg=TEXT_MUTED,
            anchor="e",
            padx=14,
            pady=4,
        )
        self.preview_label.pack(fill=tk.X)

        # Primary input / result display
        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=display_font,
            bg=BG_DISPLAY,
            fg=TEXT_LIGHT,
            anchor="e",
            padx=14,
            pady=10,
        )
        self.display_label.pack(fill=tk.X)

        # Keypad Grid Frame
        keypad_frame = tk.Frame(self.root, bg=BG_MAIN)
        keypad_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        for i in range(6):
            keypad_frame.rowconfigure(i, weight=1)
        for j in range(4):
            keypad_frame.columnconfigure(j, weight=1)

        # Button Layout: (Text, Row, Col, Command, Type)
        button_definitions = [
            ("C", 0, 0, self.clear, "clear"),
            ("⌫", 0, 1, self.backspace, "clear"),
            ("√", 0, 2, lambda: self.append_op("sqrt("), "op"),
            ("^", 0, 3, lambda: self.append_op("^"), "op"),

            ("(", 1, 0, lambda: self.append_char("("), "op"),
            (")", 1, 1, lambda: self.append_char(")"), "op"),
            ("//", 1, 2, lambda: self.append_op("//"), "op"),
            ("÷", 1, 3, lambda: self.append_op("÷"), "op"),

            ("7", 2, 0, lambda: self.append_char("7"), "num"),
            ("8", 2, 1, lambda: self.append_char("8"), "num"),
            ("9", 2, 2, lambda: self.append_char("9"), "num"),
            ("×", 2, 3, lambda: self.append_op("×"), "op"),

            ("4", 3, 0, lambda: self.append_char("4"), "num"),
            ("5", 3, 1, lambda: self.append_char("5"), "num"),
            ("6", 3, 2, lambda: self.append_char("6"), "num"),
            ("-", 3, 3, lambda: self.append_op("-"), "op"),

            ("1", 4, 0, lambda: self.append_char("1"), "num"),
            ("2", 4, 1, lambda: self.append_char("2"), "num"),
            ("3", 4, 2, lambda: self.append_char("3"), "num"),
            ("+", 4, 3, lambda: self.append_op("+"), "op"),

            ("±", 5, 0, self.toggle_sign, "num"),
            ("0", 5, 1, lambda: self.append_char("0"), "num"),
            (".", 5, 2, lambda: self.append_char("."), "num"),
            ("=", 5, 3, self.calculate_result, "equal"),
        ]

        for text, row, col, cmd, b_type in button_definitions:
            if b_type == "num":
                btn = ModernButton(
                    keypad_frame,
                    text=text,
                    font=btn_font,
                    bg=BG_BTN_NUM,
                    fg=TEXT_LIGHT,
                    normal_bg=BG_BTN_NUM,
                    hover_bg=BG_BTN_NUM_HOVER,
                    command=cmd,
                )
            elif b_type == "op":
                btn = ModernButton(
                    keypad_frame,
                    text=text,
                    font=btn_font,
                    bg=BG_BTN_OP,
                    fg=BG_BTN_ACCENT,
                    normal_bg=BG_BTN_OP,
                    hover_bg=BG_BTN_OP_HOVER,
                    command=cmd,
                )
            elif b_type == "clear":
                btn = ModernButton(
                    keypad_frame,
                    text=text,
                    font=btn_font,
                    bg=BG_BTN_OP,
                    fg=BG_BTN_CLEAR,
                    normal_bg=BG_BTN_OP,
                    hover_bg=BG_BTN_CLEAR_HOVER,
                    command=cmd,
                )
            elif b_type == "equal":
                btn = ModernButton(
                    keypad_frame,
                    text=text,
                    font=btn_font,
                    bg=BG_BTN_EQUAL,
                    fg=TEXT_DARK,
                    normal_bg=BG_BTN_EQUAL,
                    hover_bg=BG_BTN_EQUAL_HOVER,
                    command=cmd,
                )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def _bind_keys(self):
        """Bind keyboard events for seamless user interaction."""
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self.calculate_result())
        self.root.bind("<KP_Enter>", lambda e: self.calculate_result())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear())

    def _on_key_press(self, event):
        char = event.char
        if char in "0123456789.":
            self.append_char(char)
        elif char in "+-*/%^()":
            symbol = "×" if char == "*" else ("÷" if char == "/" else char)
            self.append_op(symbol)
        elif char == "=":
            self.calculate_result()

    def update_display(self):
        txt = self.current_expr if self.current_expr else "0"
        # Truncate visually if extremely long
        if len(txt) > 22:
            self.display_label.configure(font=font.Font(family="Segoe UI", size=18, weight="bold"))
        elif len(txt) > 14:
            self.display_label.configure(font=font.Font(family="Segoe UI", size=22, weight="bold"))
        else:
            self.display_label.configure(font=font.Font(family="Segoe UI", size=26, weight="bold"))
        self.display_label.configure(text=txt)

    def append_char(self, char: str):
        if self.just_evaluated:
            if char in "0123456789.":
                self.current_expr = ""
            self.just_evaluated = False

        if char == ".":
            # Avoid duplicate decimals in current token
            tokens = self.current_expr.replace("+", " ").replace("-", " ").replace("×", " ").replace("÷", " ").replace("^", " ").replace("//", " ").split()
            if tokens and "." in tokens[-1]:
                return

        self.current_expr += char
        self.update_display()

    def append_op(self, op: str):
        self.just_evaluated = False
        if not self.current_expr:
            if op == "-":
                self.current_expr = "-"
                self.update_display()
                return
            if op == "sqrt(":
                self.current_expr = "sqrt("
                self.update_display()
                return
            return

        # If last char is operator, replace with new operator (except parentheses)
        last_char = self.current_expr[-1]
        if last_char in "+-×÷%^":
            self.current_expr = self.current_expr[:-1] + op
        else:
            self.current_expr += op
        self.update_display()

    def toggle_sign(self):
        if not self.current_expr or self.current_expr == "0":
            return
        if self.current_expr.startswith("-"):
            self.current_expr = self.current_expr[1:]
        else:
            self.current_expr = "-" + self.current_expr
        self.update_display()

    def clear(self):
        self.current_expr = ""
        self.preview_label.configure(text="")
        self.just_evaluated = False
        self.update_display()

    def backspace(self):
        if self.just_evaluated:
            self.clear()
            return
        if self.current_expr:
            # If removing "sqrt(", pop 5 characters
            if self.current_expr.endswith("sqrt("):
                self.current_expr = self.current_expr[:-5]
            elif self.current_expr.endswith("//"):
                self.current_expr = self.current_expr[:-2]
            else:
                self.current_expr = self.current_expr[:-1]
            self.update_display()

    def calculate_result(self):
        if not self.current_expr:
            return

        expr = self.current_expr
        # Auto-close open parentheses
        open_parens = expr.count("(")
        close_parens = expr.count(")")
        if open_parens > close_parens:
            expr += ")" * (open_parens - close_parens)

        try:
            result = evaluate_expression(expr)
            self.preview_label.configure(text=f"{expr} =")
            self.current_expr = str(result)
            self.just_evaluated = True
            self.update_display()
        except ZeroDivisionError:
            self.preview_label.configure(text=f"{expr} =")
            self.display_label.configure(text="Cannot divide by 0")
            self.current_expr = ""
            self.just_evaluated = True
        except ValueError as e:
            self.preview_label.configure(text="Error")
            self.display_label.configure(text=str(e)[:24])
            self.current_expr = ""
            self.just_evaluated = True
        except Exception as e:
            self.preview_label.configure(text="Error")
            self.display_label.configure(text="Invalid Expression")
            self.current_expr = ""
            self.just_evaluated = True

    def show_history_window(self):
        """Open a popup window displaying calculation history."""
        hist_win = tk.Toplevel(self.root)
        hist_win.title("Calculation History")
        hist_win.geometry("340x420")
        hist_win.minsize(300, 300)
        hist_win.configure(bg=BG_MAIN)

        title_lbl = tk.Label(
            hist_win,
            text="Calculation History",
            font=font.Font(family="Segoe UI", size=13, weight="bold"),
            bg=BG_MAIN,
            fg=TEXT_LIGHT,
            pady=10,
        )
        title_lbl.pack()

        # Text list box with scrollbar
        frame = tk.Frame(hist_win, bg=BG_MAIN)
        frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            bg=BG_DISPLAY,
            fg=TEXT_LIGHT,
            font=font.Font(family="Consolas", size=11),
            selectbackground=BG_BTN_NUM_HOVER,
            highlightthickness=0,
            bd=0,
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        entries = history.get_all()
        if not entries:
            listbox.insert(tk.END, "No history available.")
        else:
            for entry in entries:
                listbox.insert(tk.END, str(entry))

        def clear_hist():
            history.clear()
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, "History cleared.")

        btn_frame = tk.Frame(hist_win, bg=BG_MAIN)
        btn_frame.pack(fill=tk.X, padx=14, pady=10)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear History",
            font=font.Font(family="Segoe UI", size=10),
            bg=BG_BTN_CLEAR,
            fg=TEXT_DARK,
            activebackground=BG_BTN_CLEAR_HOVER,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4,
            command=clear_hist,
        )
        clear_btn.pack(side=tk.LEFT)

        close_btn = tk.Button(
            btn_frame,
            text="Close",
            font=font.Font(family="Segoe UI", size=10),
            bg=BG_BTN_NUM,
            fg=TEXT_LIGHT,
            activebackground=BG_BTN_NUM_HOVER,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4,
            command=hist_win.destroy,
        )
        close_btn.pack(side=tk.RIGHT)


def run_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
