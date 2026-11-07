import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "task" / "scripts" / "find_repo.py"


class FindRepoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.realpath(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, *parts):
        os.makedirs(os.path.join(self.root, *parts))

    def find(self, name="x"):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), self.root, name],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.splitlines()

    def test_direct(self):
        self.make("x", ".git")
        self.assertEqual(self.find(), [os.path.join(self.root, "x")])

    def test_nested(self):
        self.make("org", "x", ".git")
        self.assertEqual(self.find(), [os.path.join(self.root, "org", "x")])

    def test_two_matches(self):
        self.make("a", "x", ".git")
        self.make("b", "x", ".git")
        self.assertEqual(self.find(), [os.path.join(self.root, "a", "x"),
                                       os.path.join(self.root, "b", "x")])

    def test_not_a_repo(self):
        self.make("x")
        self.assertEqual(self.find(), [])

    def test_too_deep(self):
        self.make("a", "b", "x", ".git")
        self.assertEqual(self.find(), [])

    def test_missing_folder(self):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), "/nonexistent-rabbit", "x"],
                           capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
