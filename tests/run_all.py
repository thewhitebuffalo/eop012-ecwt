"""Single entry point for the whole test suite (stdlib only).

Runs every test file in this directory in a subprocess so the two
script-style suites (custom ``main()``) and the unittest suite all count,
and one failure doesn't mask the others.

Usage:  python tests/run_all.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent


def main() -> int:
    failures = []
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    for tf in test_files:
        proc = subprocess.run([sys.executable, str(tf)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        status = "PASS" if proc.returncode == 0 else "FAIL"
        tail = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
        print(f"[{status}] {tf.name}: {tail}")
        if proc.returncode != 0:
            failures.append(tf.name)
            print(proc.stdout)
    if failures:
        print(f"\n{len(failures)}/{len(test_files)} test files FAILED: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(test_files)} test files passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
