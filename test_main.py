import pytest
import sys
from main import unified_diff_from_strings, main


class TestUnifiedDiffFromStrings:
    """Tests for the unified_diff_from_strings function."""

    def test_identical_lines_gives_empty_string(self):
        """No diff when the two sequences are identical."""
        lines = ["a\n", "b\n", "c\n"]
        result = unified_diff_from_strings(lines, lines)
        assert result == ""

    def test_empty_inputs(self):
        """Both inputs empty produce empty diff."""
        result = unified_diff_from_strings([], [])
        assert result == ""

    def test_difference_produces_expected_unified_diff(self):
        """Diff output contains standard unified diff elements."""
        a = ["line1\n", "line2\n", "line3\n"]
        b = ["line1\n", "line2 changed\n", "line3\n"]
        diff = unified_diff_from_strings(a, b)

        # Should contain file headers and hunk markers
        assert "--- a" in diff
        assert "+++ b" in diff
        assert "@@" in diff
        # Should show the removed and added lines
        assert "-line2" in diff
        assert "+line2 changed" in diff

    def test_context_parameter_affects_output(self):
        """Larger context includes more surrounding lines."""
        a = ["a\n", "b\n", "c\n", "d\n", "e\n"]
        b = ["a\n", "B\n", "c\n", "d\n", "e\n"]
        diff0 = unified_diff_from_strings(a, b, context=0)
        diff3 = unified_diff_from_strings(a, b, context=3)

        # With context=0, only the changed line appears (plus header)
        assert "+B" in diff0
        # The unchanged line 'c' should not appear in a zero‑context diff
        assert " c" not in diff0

        # With context=3, neighbouring lines are included
        assert " c" in diff3
        assert " d" in diff3

    def test_edge_case_added_lines_in_empty_file(self):
        """All lines added when comparing empty list to a non‑empty list."""
        a: list[str] = []
        b = ["new line\n"]
        diff = unified_diff_from_strings(a, b)
        assert "@@" in diff
        assert "+new line" in diff


class TestMainFunction:
    """Tests for the main() entry point."""

    def test_default_run_prints_diff(self, capsys, monkeypatch):
        """With no arguments, the built‑in samples produce a diff."""
        monkeypatch.setattr(sys, "argv", ["main.py"])
        main()
        captured = capsys.readouterr()

        # The diff is not identical
        assert "Files are identical." not in captured.out
        # Warning should not appear when no file arguments are given
        assert "Warning" not in captured.err
        # The diff includes the standard unified diff markers
        assert "--- sample_a.txt" in captured.out
        assert "+++ sample_b.txt" in captured.out

    def test_identical_diff_triggers_message(self, capsys, monkeypatch):
        """When diff is empty, main prints 'Files are identical.'"""
        # Monkey‑patch unified_diff_from_strings to return an empty diff
        monkeypatch.setattr(
            "main.unified_diff_from_strings",
            lambda *a, **kw: ""
        )
        monkeypatch.setattr(sys, "argv", ["main.py"])
        main()
        captured = capsys.readouterr()
        assert "Files are identical." in captured.out

    def test_context_cli_argument_is_respected(self, capsys, monkeypatch):
        """The -c / --context option changes the amount of context."""
        monkeypatch.setattr(sys, "argv", ["main.py", "-c", "0"])
        main()
        captured = capsys.readouterr()

        # With zero context, unchanged lines around the change should be absent.
        # The built‑in samples contain line 4, which is unchanged; it must NOT appear.
        assert " line 4" not in captured.out
        # But a hunk header is still printed
        assert "@@" in captured.out

    def test_external_file_warning(self, capsys, monkeypatch):
        """Providing file arguments triggers the warning (and still uses samples)."""
        monkeypatch.setattr(sys, "argv", ["main.py", "file1.txt", "file2.txt"])
        main()
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "External file comparison is not supported" in captured.err
        # It still prints the sample diff (not identical)
        assert "--- sample_a.txt" in captured.out