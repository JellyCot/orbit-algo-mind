"""Tests for orbit-algo-mind agent."""

import pytest
from algorithm.agent import AlgorithmAgent
from algorithm.models import SolveRequest, TestCase
from algorithm.code_executor import execute_code, run_python


@pytest.mark.asyncio
async def test_agent_mock_mode():
    agent = AlgorithmAgent()
    assert agent.client.mock_mode is True
    request = SolveRequest(problem="Two Sum", language="python")
    result = await agent.solve(request)
    assert result.solution is not None
    assert result.solution.approach == "Hash Map"


@pytest.mark.asyncio
async def test_agent_hints_mode():
    agent = AlgorithmAgent()
    request = SolveRequest(problem="Two Sum", language="python", mode="hints")
    result = await agent.solve(request)
    assert "Hints" in result.solution.explanation


@pytest.mark.asyncio
async def test_agent_cpp():
    agent = AlgorithmAgent()
    request = SolveRequest(problem="Two Sum", language="cpp")
    result = await agent.solve(request)
    assert result.solution.language == "python"  # mock returns python regardless


def test_python_executor_basic():
    code = """def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
        seen[num] = i
    return []

print(two_sum([2,7,11,15], 9))"""
    tcs = [TestCase(input="[2,7,11,15], 9", expected="[0, 1]")]
    results = run_python(code, tcs)
    assert len(results) == 1
    assert results[0]["passed"]
    assert "time_ms" in results[0]


def test_python_executor_multiple_cases():
    code = """def add(a, b):
    return a + b

print(add(1, 2))"""
    tcs = [
        TestCase(input="1, 2", expected="3"),
        TestCase(input="0, 0", expected="0"),
        TestCase(input="-1, 1", expected="0"),
    ]
    results = run_python(code, tcs)
    assert len(results) == 3
    assert all(r["passed"] for r in results)


def test_python_executor_failure():
    code = "print(42)"
    tcs = [TestCase(input="", expected="99")]
    results = run_python(code, tcs)
    assert len(results) == 1
    assert not results[0]["passed"]


def test_python_executor_timeout():
    code = "import time; time.sleep(20); print('done')"
    tcs = [TestCase(input="", expected="done")]
    results = run_python(code, tcs)
    assert len(results) == 1
    assert not results[0]["passed"]
    assert "TIMEOUT" in results[0]["actual"]


def test_unsupported_language():
    tcs = [TestCase(input="1", expected="1")]
    results = execute_code("print(1)", "rust", tcs)
    assert len(results) == 1
    assert not results[0]["passed"]
    assert "UNSUPPORTED" in results[0]["actual"]


def test_execute_code_dispatch():
    tcs = [TestCase(input="", expected="3")]
    results = execute_code("print(1+2)", "python", tcs)
    assert len(results) == 1
    assert results[0]["passed"]
