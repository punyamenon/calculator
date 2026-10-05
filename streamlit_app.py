"""Streamlit Web Application for the Python Calculator.

Features:
- Interactive keypad calculator with live OLED-styled display
- Direct formula & expression evaluator with AST safety
- Scientific math tools (Square root, Powers, Factorials, Prime check, GCD/LCM)
- Multi-category Unit Converter (Length, Mass, Temperature, Digital Data)
- Calculation history with re-use and export capabilities
- Seamless deployment on Streamlit Community Cloud (share.streamlit.io)
"""

import math
from datetime import datetime
import streamlit as st

from calculator import (
    evaluate_expression,
    format_number,
    square_root,
    history,
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Python Calculator Pro",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom Styling (CSS)
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 16px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.4);
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .app-header h1 {
        font-weight: 800;
        font-size: 2.1rem;
        letter-spacing: -0.02em;
        margin: 0;
        color: #ffffff;
    }
    .app-header p {
        color: #c7d2fe;
        font-size: 1rem;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .badge-container {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #e0e7ff;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Calculator Display Card */
    .calc-screen {
        background: #090d16;
        border: 2px solid #1e293b;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6), 0 8px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    .calc-screen-expr {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        color: #94a3b8;
        min-height: 1.6rem;
        text-align: right;
        word-break: break-all;
    }
    .calc-screen-res {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        color: #38bdf8;
        text-align: right;
        min-height: 3.2rem;
        line-height: 1.2;
        word-break: break-all;
        text-shadow: 0 0 16px rgba(56, 189, 248, 0.35);
    }

    /* Keypad Button Styling */
    div[data-testid="stButton"] > button {
        width: 100%;
        height: 3.4rem;
        font-size: 1.25rem;
        font-weight: 600;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.15s ease-in-out;
        font-family: 'JetBrains Mono', monospace;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(1px);
    }

    /* History card styling */
    .history-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .history-card:hover {
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(99, 102, 241, 0.4);
    }
</style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "calc_expr" not in st.session_state:
    st.session_state.calc_expr = ""
if "calc_res" not in st.session_state:
    st.session_state.calc_res = "0"
if "history_log" not in st.session_state:
    st.session_state.history_log = []
if "last_action" not in st.session_state:
    st.session_state.last_action = None


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def apply_precision(val_str: str, prec: int) -> str:
    """Format string result with given decimal precision if numeric."""
    try:
        val = float(val_str)
        if prec == -1 or val.is_integer():
            return str(int(val)) if val.is_integer() else f"{val:.10g}"
        return f"{val:.{prec}f}".rstrip("0").rstrip(".")
    except (ValueError, TypeError):
        return str(val_str)


def handle_keypad_press(key: str, precision: int):
    """Handle keypad button clicks."""
    current = st.session_state.calc_expr

    if key == "C":
        # Clear all
        st.session_state.calc_expr = ""
        st.session_state.calc_res = "0"
        st.session_state.last_action = "clear"

    elif key == "CE":
        # Clear entry
        st.session_state.calc_expr = ""
        st.session_state.last_action = "ce"

    elif key == "⌫":
        # Backspace
        if current:
            st.session_state.calc_expr = current[:-1]
        st.session_state.last_action = "backspace"

    elif key == "=":
        # Calculate
        if not current.strip():
            return
        try:
            raw_res = evaluate_expression(current)
            formatted = apply_precision(str(raw_res), precision)
            st.session_state.calc_res = formatted
            # Append to history log
            st.session_state.history_log.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "expression": current,
                "result": formatted,
            })
            st.session_state.last_action = "equals"
        except Exception as e:
            st.session_state.calc_res = f"Error: {e}"
            st.session_state.last_action = "error"

    elif key == "√":
        # Append square root function
        st.session_state.calc_expr = f"{current}sqrt(" if current else "sqrt("
        st.session_state.last_action = "sqrt"

    elif key == "%":
        # Modulo
        st.session_state.calc_expr = f"{current} % "
        st.session_state.last_action = "mod"

    elif key == "//":
        # Floor division
        st.session_state.calc_expr = f"{current} // "
        st.session_state.last_action = "floordiv"

    elif key in ("+", "-", "×", "÷", "^"):
        op_map = {"×": "*", "÷": "/", "^": "^"}
        op_char = op_map.get(key, key)
        # Add space for readability
        st.session_state.calc_expr = f"{current} {op_char} "
        st.session_state.last_action = "op"

    else:
        # Number or decimal or bracket
        st.session_state.calc_expr = current + key
        st.session_state.last_action = "input"


# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
st.markdown(
    """
<div class="app-header">
    <h1>🧮 Python Calculator Pro</h1>
    <p>A full-featured mathematical engine with Safe AST evaluation, modern interactive keypad, and scientific tools.</p>
    <div class="badge-container">
        <span class="badge">⚡ Safe AST Parsing</span>
        <span class="badge">🧪 100% Test Coverage</span>
        <span class="badge">🌐 Cloud Ready</span>
        <span class="badge">🐍 Python 3.12</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Controls & Settings
# ---------------------------------------------------------
with st.sidebar:
    st.subheader("⚙️ Settings")
    prec_option = st.selectbox(
        "Decimal Precision",
        options=["Auto / Dynamic", "2 decimals (0.01)", "4 decimals (0.0001)", "6 decimals (0.000001)"],
        index=0,
    )
    prec_map = {
        "Auto / Dynamic": -1,
        "2 decimals (0.01)": 2,
        "4 decimals (0.0001)": 4,
        "6 decimals (0.000001)": 6,
    }
    precision = prec_map[prec_option]

    st.divider()

    st.subheader("🚀 Deployment Guide")
    st.markdown(
        """
    **Host this on Streamlit Cloud:**
    1. Fork or push to your [GitHub repository](https://github.com/punyamenon/calculator).
    2. Go to **[share.streamlit.io](https://share.streamlit.io)**.
    3. Click **New app** and select:
       - **Repository:** `punyamenon/calculator`
       - **Branch:** `main`
       - **Main file path:** `streamlit_app.py`
    4. Click **Deploy!** 🎈
    """
    )

    st.divider()
    st.caption("Built with Python, Tkinter, AST & Streamlit.")

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_calc, tab_advanced, tab_converter, tab_history = st.tabs([
    "📱 Interactive Keypad",
    "🔬 Advanced Expression Evaluator",
    "📐 Math Tools & Converter",
    "📜 History Log",
])

# =========================================================
# TAB 1: INTERACTIVE KEYPAD
# =========================================================
with tab_calc:
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        # OLED Calculator Screen
        display_expr = st.session_state.calc_expr if st.session_state.calc_expr else "0"
        display_res = st.session_state.calc_res

        st.markdown(
            f"""
        <div class="calc-screen">
            <div class="calc-screen-expr">{display_expr}</div>
            <div class="calc-screen-res">{display_res}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Quick Synchronized Text Input
        col_txt_in, col_calc_btn = st.columns([3, 1])
        with col_txt_in:
            manual_input = st.text_input(
                "Type expression or use keypad below:",
                value=st.session_state.calc_expr,
                key="manual_expr_field",
                placeholder="e.g. sqrt(144) + 2^5 * 4",
                label_visibility="collapsed",
            )
            # Sync if user typed in text box
            if manual_input != st.session_state.calc_expr and manual_input.strip() != "":
                st.session_state.calc_expr = manual_input
        with col_calc_btn:
            if st.button("Evaluate ⏎", key="manual_eval_btn", type="primary", use_container_width=True):
                handle_keypad_press("=", precision)
                st.rerun()

        # Keypad Grid Layout
        # Row 1: Extra math functions
        r0_c1, r0_c2, r0_c3, r0_c4 = st.columns(4)
        with r0_c1:
            if st.button("√ (sqrt)", key="btn_sqrt", use_container_width=True):
                handle_keypad_press("√", precision)
                st.rerun()
        with r0_c2:
            if st.button("^ (pow)", key="btn_pow", use_container_width=True):
                handle_keypad_press("^", precision)
                st.rerun()
        with r0_c3:
            if st.button("// (div)", key="btn_fdiv", use_container_width=True):
                handle_keypad_press("//", precision)
                st.rerun()
        with r0_c4:
            if st.button("% (mod)", key="btn_mod", use_container_width=True):
                handle_keypad_press("%", precision)
                st.rerun()

        # Row 2: Clear & Backspace
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
        with r1_c1:
            if st.button("C", key="btn_c", use_container_width=True):
                handle_keypad_press("C", precision)
                st.rerun()
        with r1_c2:
            if st.button("CE", key="btn_ce", use_container_width=True):
                handle_keypad_press("CE", precision)
                st.rerun()
        with r1_c3:
            if st.button("⌫", key="btn_back", use_container_width=True):
                handle_keypad_press("⌫", precision)
                st.rerun()
        with r1_c4:
            if st.button("÷", key="btn_div", use_container_width=True):
                handle_keypad_press("÷", precision)
                st.rerun()

        # Row 3: 7 8 9 *
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        with r2_c1:
            if st.button("7", key="btn_7", use_container_width=True):
                handle_keypad_press("7", precision)
                st.rerun()
        with r2_c2:
            if st.button("8", key="btn_8", use_container_width=True):
                handle_keypad_press("8", precision)
                st.rerun()
        with r2_c3:
            if st.button("9", key="btn_9", use_container_width=True):
                handle_keypad_press("9", precision)
                st.rerun()
        with r2_c4:
            if st.button("×", key="btn_mul", use_container_width=True):
                handle_keypad_press("×", precision)
                st.rerun()

        # Row 4: 4 5 6 -
        r3_c1, r3_c2, r3_c3, r3_c4 = st.columns(4)
        with r3_c1:
            if st.button("4", key="btn_4", use_container_width=True):
                handle_keypad_press("4", precision)
                st.rerun()
        with r3_c2:
            if st.button("5", key="btn_5", use_container_width=True):
                handle_keypad_press("5", precision)
                st.rerun()
        with r3_c3:
            if st.button("6", key="btn_6", use_container_width=True):
                handle_keypad_press("6", precision)
                st.rerun()
        with r3_c4:
            if st.button("-", key="btn_sub", use_container_width=True):
                handle_keypad_press("-", precision)
                st.rerun()

        # Row 5: 1 2 3 +
        r4_c1, r4_c2, r4_c3, r4_c4 = st.columns(4)
        with r4_c1:
            if st.button("1", key="btn_1", use_container_width=True):
                handle_keypad_press("1", precision)
                st.rerun()
        with r4_c2:
            if st.button("2", key="btn_2", use_container_width=True):
                handle_keypad_press("2", precision)
                st.rerun()
        with r4_c3:
            if st.button("3", key="btn_3", use_container_width=True):
                handle_keypad_press("3", precision)
                st.rerun()
        with r4_c4:
            if st.button("+", key="btn_add", use_container_width=True):
                handle_keypad_press("+", precision)
                st.rerun()

        # Row 6: 0 . () =
        r5_c1, r5_c2, r5_c3, r5_c4 = st.columns(4)
        with r5_c1:
            if st.button("0", key="btn_0", use_container_width=True):
                handle_keypad_press("0", precision)
                st.rerun()
        with r5_c2:
            if st.button(".", key="btn_dot", use_container_width=True):
                handle_keypad_press(".", precision)
                st.rerun()
        with r5_c3:
            if st.button("( )", key="btn_parens", use_container_width=True):
                # Smart parenthesis addition
                open_cnt = st.session_state.calc_expr.count("(")
                close_cnt = st.session_state.calc_expr.count(")")
                if open_cnt > close_cnt and (st.session_state.calc_expr and st.session_state.calc_expr[-1] not in "( +-*/^"):
                    handle_keypad_press(")", precision)
                else:
                    handle_keypad_press("(", precision)
                st.rerun()
        with r5_c4:
            if st.button("=", key="btn_eq", type="primary", use_container_width=True):
                handle_keypad_press("=", precision)
                st.rerun()

    with col_right:
        st.subheader("💡 Quick Examples")
        st.caption("Click any preset formula to load and evaluate immediately:")

        preset_examples = [
            ("Compound Precedence", "(25 + 15) * 3 / 2"),
            ("Power and Square Root", "sqrt(144) + 2^5"),
            ("Modulo and Floor Div", "100 % 7 + (45 // 4)"),
            ("Scientific Expression", "sqrt(256) * 3^3 - 100"),
            ("Parentheses Grouping", "((12 + 8) * (15 - 5)) / 4"),
        ]

        for label, expr in preset_examples:
            col_lbl, col_load = st.columns([3, 1])
            with col_lbl:
                st.code(expr, language="text")
            with col_load:
                if st.button("Load", key=f"load_preset_{label}", use_container_width=True):
                    st.session_state.calc_expr = expr
                    handle_keypad_press("=", precision)
                    st.rerun()

        st.divider()
        st.subheader("📋 Memory & Quick Action")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("Ans -> Input", use_container_width=True, help="Use current result in expression"):
                if st.session_state.calc_res and not str(st.session_state.calc_res).startswith("Error"):
                    st.session_state.calc_expr = str(st.session_state.calc_res)
                    st.rerun()
        with col_m2:
            if st.button("Clear Screen", use_container_width=True):
                handle_keypad_press("C", precision)
                st.rerun()


# =========================================================
# TAB 2: ADVANCED EXPRESSION EVALUATOR
# =========================================================
with tab_advanced:
    st.subheader("🔬 High-Precision Expression Evaluator")
    st.markdown(
        "Evaluate full-length mathematical formulas with support for nested parentheses, exponents, square roots, and complete order of operations."
    )

    adv_expr = st.text_area(
        "Enter expression:",
        value=st.session_state.calc_expr if st.session_state.calc_expr else "sqrt(625) + 3^4 * (12 - 7) / 5",
        height=100,
        key="adv_expr_area",
    )

    col_btn_eval, col_btn_clear = st.columns([1, 5])
    with col_btn_eval:
        eval_trigger = st.button("Calculate", key="adv_eval_trigger", type="primary", use_container_width=True)

    if eval_trigger or adv_expr:
        try:
            adv_res = evaluate_expression(adv_expr)
            formatted_res = apply_precision(str(adv_res), precision)

            st.success(f"### Result: **`{formatted_res}`**")

            # Explanation card
            with st.expander("🔍 Order of Operations & Evaluation Details", expanded=True):
                st.markdown(
                    f"""
                - **Expression:** `{adv_expr}`
                - **Evaluated Result:** `{formatted_res}`
                - **AST Parser:** Python Abstract Syntax Tree (`ast.Expression`)
                - **Security Guarantee:** Safe node-by-node validation; zero `eval()` vulnerabilities.
                """
                )
        except Exception as e:
            st.error(f"**Evaluation Error:** {e}")


# =========================================================
# TAB 3: MATH TOOLS & UNIT CONVERTER
# =========================================================
with tab_converter:
    st.subheader("📐 Math Tools & Multi-Unit Converter")

    conv_tab1, conv_tab2 = st.tabs(["🔄 Unit Converter", "🧮 Number Theory Tools"])

    with conv_tab1:
        category = st.selectbox("Category", ["Length", "Mass / Weight", "Temperature", "Digital Storage"])

        if category == "Length":
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                val = st.number_input("Value", value=1.0, format="%.4f")
            with col_c2:
                from_u = st.selectbox("From", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Feet", "Inches"])
            with col_c3:
                to_u = st.selectbox("To", ["Feet", "Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Inches"])

            # Conversion logic to meters
            to_meter = {
                "Meters": 1.0,
                "Kilometers": 1000.0,
                "Centimeters": 0.01,
                "Millimeters": 0.001,
                "Miles": 1609.344,
                "Feet": 0.3048,
                "Inches": 0.0254,
            }
            meters = val * to_meter[from_u]
            converted = meters / to_meter[to_u]
            st.info(f"**{val} {from_u}** = **{converted:.6g} {to_u}**")

        elif category == "Mass / Weight":
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                val = st.number_input("Value", value=1.0, format="%.4f")
            with col_c2:
                from_u = st.selectbox("From", ["Kilograms", "Grams", "Milligrams", "Pounds (lbs)", "Ounces (oz)"])
            with col_c3:
                to_u = st.selectbox("To", ["Pounds (lbs)", "Kilograms", "Grams", "Milligrams", "Ounces (oz)"])

            to_kg = {
                "Kilograms": 1.0,
                "Grams": 0.001,
                "Milligrams": 0.000001,
                "Pounds (lbs)": 0.45359237,
                "Ounces (oz)": 0.028349523,
            }
            kgs = val * to_kg[from_u]
            converted = kgs / to_kg[to_u]
            st.info(f"**{val} {from_u}** = **{converted:.6g} {to_u}**")

        elif category == "Temperature":
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                val = st.number_input("Value", value=25.0, format="%.2f")
            with col_c2:
                from_u = st.selectbox("From", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"])
            with col_c3:
                to_u = st.selectbox("To", ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"])

            # Convert to Celsius first
            if from_u == "Celsius (°C)":
                c = val
            elif from_u == "Fahrenheit (°F)":
                c = (val - 32) * 5 / 9
            else:
                c = val - 273.15

            # Convert to target
            if to_u == "Celsius (°C)":
                out = c
            elif to_u == "Fahrenheit (°F)":
                out = (c * 9 / 5) + 32
            else:
                out = c + 273.15

            st.info(f"**{val} {from_u}** = **{out:.4f} {to_u}**")

        elif category == "Digital Storage":
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                val = st.number_input("Value", value=1024.0, format="%.2f")
            with col_c2:
                from_u = st.selectbox("From", ["Bytes (B)", "Kilobytes (KB)", "Megabytes (MB)", "Gigabytes (GB)", "Terabytes (TB)"])
            with col_c3:
                to_u = st.selectbox("To", ["Megabytes (MB)", "Bytes (B)", "Kilobytes (KB)", "Gigabytes (GB)", "Terabytes (TB)"])

            bytes_map = {
                "Bytes (B)": 1,
                "Kilobytes (KB)": 1024,
                "Megabytes (MB)": 1024**2,
                "Gigabytes (GB)": 1024**3,
                "Terabytes (TB)": 1024**4,
            }
            bytes_val = val * bytes_map[from_u]
            converted = bytes_val / bytes_map[to_u]
            st.info(f"**{val} {from_u}** = **{converted:.6g} {to_u}**")

    with conv_tab2:
        col_t1, col_t2 = st.columns(2)

        with col_t1:
            st.markdown("#### 🔢 Prime & Factorial Checker")
            num_input = st.number_input("Enter positive integer:", min_value=0, max_value=10000, value=29, step=1)

            # Prime check
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(math.isqrt(n)) + 1):
                    if n % i == 0:
                        return False
                return True

            prime_status = "✅ Prime Number" if is_prime(num_input) else "❌ Not a Prime Number"
            st.write(f"- **Prime Status:** {prime_status}")

            if num_input <= 50:
                st.write(f"- **Factorial ({num_input}!):** `{math.factorial(num_input)}`")
            else:
                st.write("- **Factorial:** *(Values > 50 omitted for display)*")

        with col_t2:
            st.markdown("#### 🔗 GCD and LCM")
            num_a = st.number_input("First Number (a):", min_value=1, value=48, step=1)
            num_b = st.number_input("Second Number (b):", min_value=1, value=180, step=1)

            gcd_val = math.gcd(num_a, num_b)
            lcm_val = math.lcm(num_a, num_b)

            st.write(f"- **Greatest Common Divisor (GCD):** `{gcd_val}`")
            st.write(f"- **Least Common Multiple (LCM):** `{lcm_val}`")


# =========================================================
# TAB 4: CALCULATION HISTORY
# =========================================================
with tab_history:
    st.subheader("📜 Session Calculation History")

    if not st.session_state.history_log:
        st.info("No calculations performed yet in this session. Calculate expressions to record them here!")
    else:
        col_actions_1, col_actions_2 = st.columns([1, 4])
        with col_actions_1:
            if st.button("🗑️ Clear History", key="clear_hist_btn"):
                st.session_state.history_log = []
                st.rerun()

        # Display history items
        for idx, item in enumerate(reversed(st.session_state.history_log)):
            col_hist_txt, col_hist_btn = st.columns([4, 1])
            with col_hist_txt:
                st.markdown(
                    f"""
                <div class="history-card">
                    <div>
                        <span style="color: #94a3b8; font-size: 0.85rem;">[{item['time']}]</span>
                        <strong style="margin-left: 0.5rem; font-family: 'JetBrains Mono', monospace;">{item['expression']}</strong>
                    </div>
                    <div style="color: #38bdf8; font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 1.15rem;">
                        = {item['result']}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with col_hist_btn:
                if st.button("Load ⏎", key=f"hist_load_{idx}", use_container_width=True):
                    st.session_state.calc_expr = item["expression"]
                    st.session_state.calc_res = item["result"]
                    st.rerun()

        # Download History
        history_text = "\n".join([f"[{i['time']}] {i['expression']} = {i['result']}" for i in st.session_state.history_log])
        st.download_button(
            label="📥 Download History as Text",
            data=history_text,
            file_name="calculator_history.txt",
            mime="text/plain",
        )
