"""Tests for orbit-algo-mind agent."""

import pytest
from algorithm.agent import AlgorithmAgent
from algorithm.models import SolveRequest
from algorithm.code_executor import execute_code, run_python
from algorithm.models import TestCase


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


def test_python_executor():
    code = "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        comp = target - num\n        if comp in seen:\n            return [seen[comp], i]\n        seen[num] = i\n    return []\n\nprint(two_sum([2,7,11,15], 9))"
    tcs = [TestCase(input="[2,7,11,15], 9", expected="[0, 1]")]
    results = run_python(code, tcs)
    assert len(results) == 1
    assert results[0]["passed"]
