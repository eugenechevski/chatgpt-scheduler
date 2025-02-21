#!/usr/bin/env python3
"""
test_scheduler.py

This script finds all .in files in the current directory, runs the scheduler-gpt.py
script on each input file, and compares the generated output (produced by replacing the
".in" extension with "out") against the expected .out file.

Usage:
    python3 test_scheduler.py
"""

import glob
import subprocess
import os
import sys
import difflib

def run_test(in_file):
    # Derive expected and generated output filenames.
    base, _ = os.path.splitext(in_file)
    expected_file = base + ".out"
    generated_file = in_file.replace(".in", ".generated.out")
    
    if not os.path.exists(expected_file):
        print(f"Expected output file {expected_file} not found for input {in_file}. Skipping test.")
        return False

    # Run the scheduler script.
    result = subprocess.run(["python3", "scheduler-gpt.py", in_file],
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running scheduler-gpt.py on {in_file}:")
        print(result.stdout)
        print(result.stderr)
        return False

    if not os.path.exists(generated_file):
        print(f"Generated output file {generated_file} not found for input {in_file}.")
        return False

    with open(generated_file, "r") as f:
        generated = f.read()
    with open(expected_file, "r") as f:
        expected = f.read()

    if generated == expected:
        print(f"Test {in_file} passed.")
        return True
    else:
        print(f"Test {in_file} failed. Differences:")
        diff = difflib.unified_diff(
            expected.splitlines(keepends=True),
            generated.splitlines(keepends=True),
            fromfile="expected",
            tofile="generated"
        )
        print("".join(diff))
        return False

def main():
    in_files = glob.glob("*.in")
    if not in_files:
        print("No .in files found in the current directory.")
        sys.exit(1)
    
    all_passed = True
    for in_file in in_files:
        print(f"\nRunning test for {in_file}...")
        if not run_test(in_file):
            all_passed = False
    
    if all_passed:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    main()
