"""Main entry point for the Python Calculator application.

Usage:
    python main.py             # Interactive mode (Terminal CLI with GUI launch option)
    python main.py --gui       # Directly launch Desktop GUI
    python main.py --cli       # Directly launch Terminal CLI
    python main.py -e "12*4"   # Evaluate expression directly from command line
"""

import argparse
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from calculator import evaluate_expression
from cli import main_cli


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Python Calculator - Basic & Advanced Mathematical Operations",
        epilog="Examples:\n"
               "  python main.py --gui\n"
               "  python main.py --cli\n"
               "  python main.py -e \"(25 + 15) * 3 / 2\"\n"
               "  python main.py -e \"sqrt(144) + 2^5\"",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Launch modern Desktop GUI calculator",
    )
    parser.add_argument(
        "--cli", "-c",
        action="store_true",
        help="Launch interactive terminal CLI",
    )
    parser.add_argument(
        "--eval", "-e",
        type=str,
        metavar="EXPR",
        help="Evaluate a single mathematical expression and print result",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Direct evaluation mode
    if args.eval:
        try:
            result = evaluate_expression(args.eval)
            print(result)
            sys.exit(0)
        except Exception as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)

    # Directly launch GUI
    if args.gui:
        try:
            from gui import run_gui
            run_gui()
            sys.exit(0)
        except Exception as e:
            print(f"Failed to launch GUI: {e}. Falling back to CLI mode.")
            main_cli()
            sys.exit(0)

    # Directly launch CLI
    if args.cli:
        main_cli()
        sys.exit(0)

    # Default interactive launcher
    print("=" * 48)
    print("               PYTHON CALCULATOR                ")
    print("=" * 48)
    print("Choose interface:")
    print("  [1] Interactive Terminal CLI")
    print("  [2] Modern Desktop GUI (Tkinter)")
    print("  [Q] Exit")

    while True:
        try:
            choice = input("\nEnter choice [1/2/Q] (default: 1): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            sys.exit(0)

        if not choice or choice == "1":
            main_cli()
            break
        elif choice == "2":
            try:
                from gui import run_gui
                print("Launching Desktop GUI...")
                run_gui()
                break
            except Exception as e:
                print(f"Could not open GUI: {e}. Opening CLI instead.")
                main_cli()
                break
        elif choice.upper() in ("Q", "QUIT", "EXIT"):
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or Q.")


if __name__ == "__main__":
    main()
