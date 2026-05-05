import difflib
import sys
import argparse
from typing import List, Optional


def unified_diff_from_strings(a: List[str], b: List[str],
                              fromfile: str = 'a', tofile: str = 'b',
                              context: int = 3) -> str:
    """
    Generate a unified diff string between two sequences of lines.
    """
    diff = difflib.unified_diff(a, b,
                                fromfile=fromfile,
                                tofile=tofile,
                                lineterm='',
                                n=context)
    return '\n'.join(diff)


def main() -> None:
    # ---- internal sample texts for demonstration ----
    sample_a = [
        "This is line 1.\n",
        "This is line 2.\n",
        "This is line 3 to be modified.\n",
        "This is line 4.\n",
        "This is line 5.\n",
        "This is line 6.\n",
        "This is line 7 that stays.\n",
    ]
    sample_b = [
        "This is line 1.\n",
        "This is line 2.\n",
        "This is line 3 modified.\n",
        "This is line 4.\n",
        "This is added after 4.\n",
        "This is line 5.\n",
        "This is line 7 that stays.\n",
    ]

    # ---- argument parsing (safe, default to internal samples) ----
    parser = argparse.ArgumentParser(
        description="Line-by-line unified diff tool (uses difflib)."
    )
    parser.add_argument(
        'file1', nargs='?', default=None,
        help='First file to compare (default: built-in sample a)'
    )
    parser.add_argument(
        'file2', nargs='?', default=None,
        help='Second file to compare (default: built-in sample b)'
    )
    parser.add_argument(
        '-c', '--context', type=int, default=3,
        help='Number of context lines (default: 3)'
    )

    # Ensure main() runs without arguments (sys.argv may contain only the script name)
    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else [])

    # ---- decide which lines to compare ----
    # External file reading is not allowed in this sandbox; always use built-in samples.
    # (Original file‑reading logic used open(), which is blocked.)
    if args.file1 or args.file2:
        print(
            "Warning: External file comparison is not supported in this environment. "
            "Using built‑in samples.",
            file=sys.stderr
        )
    a_lines = sample_a
    b_lines = sample_b
    fromfile = 'sample_a.txt'
    tofile = 'sample_b.txt'

    # ---- compute and print diff ----
    diff_output = unified_diff_from_strings(
        a_lines, b_lines,
        fromfile=fromfile,
        tofile=tofile,
        context=args.context
    )
    if diff_output:
        print(diff_output)
    else:
        print("Files are identical.")


if __name__ == '__main__':
    main()