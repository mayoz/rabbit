import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "task", "scripts"))
import ci_wait  # noqa: E402


def c(name, bucket):
    return {"name": name, "bucket": bucket}


class DecideTest(unittest.TestCase):
    def test_waiting_check_is_left_out(self):
        checks = [c("build", "pass"), c("e2e/staging", "pending"), c("Release Gate", "fail")]
        self.assertEqual(ci_wait.decide(checks, ["e2e/staging", "release gate"]),
                         ("passed", ["e2e/staging", "Release Gate"]))

    def test_pending_other_check_keeps_waiting(self):
        checks = [c("build", "pending"), c("e2e/staging", "pending")]
        self.assertEqual(ci_wait.decide(checks, ["e2e/staging"])[0], "pending")

    def test_failure_names_the_check(self):
        checks = [c("lint", "fail"), c("build", "pending")]
        self.assertEqual(ci_wait.decide(checks, []), ("failed", ["lint"]))

    def test_skipping_and_cancel(self):
        self.assertEqual(ci_wait.decide([c("a", "skipping")], [])[0], "passed")
        self.assertEqual(ci_wait.decide([c("a", "cancel")], []), ("failed", ["a"]))

    def test_no_checks(self):
        self.assertEqual(ci_wait.decide([], []), ("none", []))
        self.assertEqual(ci_wait.decide([c("e2e/staging", "pending")], ["e2e/staging"]),
                         ("none", ["e2e/staging"]))

    def test_line(self):
        self.assertEqual(ci_wait.line("passed", ["e2e/staging"]), "passed waiting: e2e/staging")
        self.assertEqual(ci_wait.line("failed", ["lint"]), "failed lint")
        self.assertEqual(ci_wait.line("none", []), "passed none")


if __name__ == "__main__":
    unittest.main()
