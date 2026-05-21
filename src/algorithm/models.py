"""Data models for algorithm agent."""

from pydantic import BaseModel, Field


class Problem(BaseModel):
    title: str
    description: str
    difficulty: str = "medium"
    constraints: list[str] = Field(default_factory=list)
    examples: list[dict] = Field(default_factory=list)


class TestCase(BaseModel):
    input: str
    expected: str
    description: str = ""


class Solution(BaseModel):
    approach: str
    language: str
    code: str
    complexity_time: str
    complexity_space: str
    explanation: str
    test_cases: list[TestCase] = Field(default_factory=list)


class BenchmarkResult(BaseModel):
    language: str
    time_ms: float
    memory_mb: float
    test_cases_passed: int
    test_cases_total: int


class SolveRequest(BaseModel):
    problem: str
    language: str = "python"
    mode: str = "full"  # full, hints, explain


class SolveResponse(BaseModel):
    solution: Solution
    benchmarks: list[BenchmarkResult] = Field(default_factory=list)
    tokens_used: int = 0
    model: str = ""
