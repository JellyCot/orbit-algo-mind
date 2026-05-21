"""Sandboxed code execution for algorithm solutions."""

import subprocess
import tempfile
import os
import time
from .models import TestCase


def run_python(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute Python code with test cases."""
    results = []
    for tc in test_cases:
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                full_code = f"{code}\n\nprint({tc.input})\n"
                f.write(full_code)
                f.flush()
                tmp_path = f.name

            start = time.monotonic()
            result = subprocess.run(
                ["python3", tmp_path],
                capture_output=True, text=True, timeout=10
            )
            elapsed_ms = (time.monotonic() - start) * 1000

            passed = result.stdout.strip() == tc.expected
            results.append({
                "input": tc.input,
                "expected": tc.expected,
                "actual": result.stdout.strip(),
                "passed": passed,
                "error": result.stderr.strip() if not passed else "",
                "time_ms": round(elapsed_ms, 2),
            })
        except subprocess.TimeoutExpired:
            results.append({
                "input": tc.input, "expected": tc.expected,
                "actual": "TIMEOUT", "passed": False,
                "error": "Time limit exceeded (10s)", "time_ms": 10000,
            })
        except Exception as e:
            results.append({
                "input": tc.input, "expected": tc.expected,
                "actual": "ERROR", "passed": False,
                "error": str(e), "time_ms": 0,
            })
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
    return results


def run_cpp(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute C++ code with test cases."""
    results = []
    exe_path = None
    src_path = None

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as f:
            f.write(code)
            f.flush()
            src_path = f.name

        exe_path = src_path + ".out"

        compile_result = subprocess.run(
            ["g++", "-o", exe_path, src_path, "-std=c++17", "-O2"],
            capture_output=True, text=True, timeout=15
        )
        if compile_result.returncode != 0:
            return [{
                "input": tc.input, "expected": tc.expected,
                "actual": "COMPILE ERROR", "passed": False,
                "error": compile_result.stderr, "time_ms": 0,
            } for tc in test_cases]

        for tc in test_cases:
            try:
                start = time.monotonic()
                result = subprocess.run(
                    [exe_path], input=tc.input, capture_output=True, text=True, timeout=10
                )
                elapsed_ms = (time.monotonic() - start) * 1000

                passed = result.stdout.strip() == tc.expected
                results.append({
                    "input": tc.input, "expected": tc.expected,
                    "actual": result.stdout.strip(), "passed": passed,
                    "error": result.stderr if not passed else "",
                    "time_ms": round(elapsed_ms, 2),
                })
            except subprocess.TimeoutExpired:
                results.append({
                    "input": tc.input, "expected": tc.expected,
                    "actual": "TIMEOUT", "passed": False,
                    "error": "Timeout (10s)", "time_ms": 10000,
                })
    finally:
        if src_path and os.path.exists(src_path):
            os.unlink(src_path)
        if exe_path and os.path.exists(exe_path):
            os.unlink(exe_path)

    return results


def run_go(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute Go code with test cases."""
    results = []
    exe_path = None
    src_path = None

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=False) as f:
            if "package " not in code:
                f.write("package main\n\nimport \"fmt\"\n\n")
            f.write(code)
            f.flush()
            src_path = f.name

        exe_path = src_path + ".out"

        compile_result = subprocess.run(
            ["go", "build", "-o", exe_path, src_path],
            capture_output=True, text=True, timeout=15,
            env={**os.environ, "GOFLAGS": "-modcacherw"}
        )
        if compile_result.returncode != 0:
            return [{
                "input": tc.input, "expected": tc.expected,
                "actual": "COMPILE ERROR", "passed": False,
                "error": compile_result.stderr, "time_ms": 0,
            } for tc in test_cases]

        for tc in test_cases:
            try:
                start = time.monotonic()
                result = subprocess.run(
                    [exe_path], input=tc.input, capture_output=True, text=True, timeout=10
                )
                elapsed_ms = (time.monotonic() - start) * 1000

                passed = result.stdout.strip() == tc.expected
                results.append({
                    "input": tc.input, "expected": tc.expected,
                    "actual": result.stdout.strip(), "passed": passed,
                    "error": result.stderr if not passed else "",
                    "time_ms": round(elapsed_ms, 2),
                })
            except subprocess.TimeoutExpired:
                results.append({
                    "input": tc.input, "expected": tc.expected,
                    "actual": "TIMEOUT", "passed": False,
                    "error": "Timeout (10s)", "time_ms": 10000,
                })
    finally:
        if src_path and os.path.exists(src_path):
            os.unlink(src_path)
        if exe_path and os.path.exists(exe_path):
            os.unlink(exe_path)

    return results


def execute_code(code: str, language: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute code in the specified language."""
    runners = {"python": run_python, "cpp": run_cpp, "go": run_go}
    runner = runners.get(language)
    if not runner:
        return [{
            "input": tc.input, "expected": tc.expected,
            "actual": "UNSUPPORTED", "passed": False,
            "error": f"Language '{language}' not supported. Use: python, cpp, go",
            "time_ms": 0,
        } for tc in test_cases]
    return runner(code, test_cases)
