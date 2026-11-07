import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "check_line_width", Path(__file__).resolve().parent.parent / "scripts" / "check-line-width.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class LineWidthTest(unittest.TestCase):
    def found(self, text):
        return [n for n, _ in mod.long_lines(text)]

    def test_limit(self):
        self.assertEqual(self.found("a " * 41), [1])
        self.assertEqual(self.found(("a " * 40).rstrip()), [])
        self.assertEqual(self.found("é" * 78 + " x"), [])

    def test_exempt(self):
        long = "word " * 20
        text = "\n".join(["---", "description: " + long, "---", "```", long, "```",
                          "| " + long + "|", "# " + long, "<img " + long + ">",
                          "- " + "x" * 90, "> " + "y" * 90])
        self.assertEqual(self.found(text), [])

    def test_prose_in_lists_and_quotes(self):
        self.assertEqual(self.found("- " + "word " * 20 + "\n> " + "word " * 20), [1, 2])


if __name__ == "__main__":
    unittest.main()
