"""Wait for a pull request's checks, leaving out the ones that wait for a later step.

usage: ci_wait.py <pr-url> [--waiting <check name>]...
Prints one line: `passed`, `passed none`, `passed waiting: <names>` or
`failed <names>`.
"""
import json
import subprocess
import sys
import time

DONE = {"pass", "skipping"}
FAILED = {"fail", "cancel"}
INTERVAL = 60
LIMIT = 3 * 60 * 60


def decide(checks, waiting):
    skip = {w.lower() for w in waiting}
    held = [ch["name"] for ch in checks if ch["name"].lower() in skip]
    rest = [ch for ch in checks if ch["name"].lower() not in skip]
    failed = [ch["name"] for ch in rest if ch["bucket"] in FAILED]
    if failed:
        return "failed", failed
    if any(ch["bucket"] not in DONE for ch in rest):
        return "pending", []
    return ("passed" if rest else "none"), held


def line(state, names):
    if state == "failed":
        return "failed " + ", ".join(names)
    if names:
        return "passed waiting: " + ", ".join(names)
    return "passed none" if state == "none" else "passed"


def checks(url):
    for extra in (["--required"], []):
        out = subprocess.run(["gh", "pr", "checks", url, *extra, "--json", "name,bucket"],
                             capture_output=True, text=True)
        try:
            found = json.loads(out.stdout or "null")
        except json.JSONDecodeError:
            found = None
        if found:
            return found
        if found is None and "checks reported" not in (out.stderr + out.stdout).lower():
            raise RuntimeError((out.stderr or out.stdout).strip() or "gh pr checks failed")
    return []


def main(argv):
    if len(argv) < 2 or len(argv) % 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    url, rest = argv[1], argv[2:]
    if any(flag != "--waiting" for flag in rest[::2]):
        print("unknown option", file=sys.stderr)
        return 2
    waiting = rest[1::2]
    start = time.monotonic()
    while True:
        try:
            state, names = decide(checks(url), waiting)
        except RuntimeError as err:
            print(f"failed gh: {err}")
            return 1
        if state != "pending":
            print(line(state, names))
            return 0
        if time.monotonic() - start > LIMIT:
            print("failed timeout: checks still running after 3 hours")
            return 1
        time.sleep(INTERVAL)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
