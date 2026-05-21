"""Sandboxed code execution for algorithm solutions."""

import subprocess
import tempfile
import os
from .models import TestCase


def run_python(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute Python code with test cases."""
    results = []
    for tc in test_cases:
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                full_code = f"{code}\n\nprint({tc.input})\n"
                f.write(full_code)
                f.flush()
                result = subprocess.run(
                    ["python3", f.name],
                    capture_output=True, text=True, timeout=10
                )
                os.unlink(f.name)
                passed = result.stdout.strip() == tc.expected
                results.append({
                    "input": tc.input,
                    "expected": tc.expected,
                    "actual": result.stdout.strip(),
                    "passed": passed,
                    "error": result.stderr.strip() if not passed else "",
                })
        except subprocess.TimeoutExpired:
            results.append({"input": tc.input, "expected": tc.expected, "actual": "TIMEOUT", "passed": False, "error": "Time limit exceeded"})
        except Exception as e:
            results.append({"input": tc.input, "expected": tc.expected, "actual": "ERROR", "passed": False, "error": str(e)})
    return results


def run_cpp(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute C++ code with test cases."""
    results = []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as f:
        f.write(code)
        f.flush()
        exe_path = f.name + ".out"
        try:
            compile_result = subprocess.run(
                ["g++", "-o", exe_path, f.name, "-std=c++17"],
                capture_output=True, text=True, timeout=15
            )
            if compile_result.returncode != 0:
                return [{"input": tc.input, "expected": tc.expected, "actual": "COMPILE ERROR", "passed": False, "error": compile_result.stderr} for tc in test_cases]

            for tc in test_cases:
                try:
                    result = subprocess.run(
                        [exe_path], input=tc.input, capture_output=True, text=True, timeout=10
                    )
                    passed = result.stdout.strip() == tc.expected
                    results.append({"input": tc.input, "expected": tc.expected, "actual": result.stdout.strip(), "passed": passed, "error": result.stderr if not passed else ""})
                except subprocess.TimeoutExpired:
                    results.append({"input": tc.input, "expected": tc.expected, "actual": "TIMEOUT", "passed": False, "error": "Timeout"})
        finally:
            os.unlink(f.name)
            if os.path.exists(exe_path):
                os.unlink(exe_path)
    return results


def run_go(code: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute Go code with test cases."""
    results = []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=False) as f:
        if "package " not in code:
            f.write("package main\n\n")
        f.write(code)
        f.flush()
        exe_path = f.name + ".out"
        try:
            compile_result = subprocess.run(
                ["go", "build", "-o", exe_path, f.name],
                capture_output=True, text=True, timeout=15, env={**os.environ, "GOFLAGS": "-modcacherw"}
            )
            if compile_result.returncode != 0:
                return [{"input": tc.input, "expected": tc.expected, "actual": "COMPILE ERROR", "passed": False, "error": compile_result.stderr} for tc in test_cases]

            for tc in test_cases:
                try:
                    result = subprocess.run(
                        [exe_path], input=tc.input, capture_output=True, text=True, timeout=10
                    )
                    passed = result.stdout.strip() == tc.expected
                    results.append({"input": tc.input, "expected": tc.expected, "actual": result.stdout.strip(), "passed": passed, "error": result.stderr if not passed else ""})
                except subprocess.TimeoutExpired:
                    results.append({"input": tc.input, "expected": tc.expected, "actual": "TIMEOUT", "passed": False, "error": "Timeout"})
        finally:
            os.unlink(f.name)
            if os.path.exists(exe_path):
                os.unlink(exe_path)
    return results


def execute_code(code: str, language: str, test_cases: list[TestCase]) -> list[dict]:
    """Execute code in the specified language."""
    runners = {"python": run_python, "cpp": run_cpp, "go": run_go}
    runner = runners.get(language)
    if not runner:
        return [{"input": tc.input, "expected": tc.expected, "actual": "UNSUPPORTED", "passed": False, "error": f"Language {language} not supported"} for tc in test_cases]
    return runner(code, test_cases)
