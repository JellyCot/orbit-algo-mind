"""Core algorithm solving and teaching agent."""

import json
from .client import MiMoClient
from .models import Problem, Solution, TestCase, BenchmarkResult, SolveRequest, SolveResponse
from .prompts.system import SYSTEM_PROMPT, HINT_PROMPT
from .code_executor import execute_code


class AlgorithmAgent:
    def __init__(self, client: MiMoClient | None = None):
        self.client = client or MiMoClient()

    async def solve(self, request: SolveRequest) -> SolveResponse:
        if request.mode == "hints":
            return await self._get_hints(request)
        return await self._full_solve(request)

    async def solve_stream(self, request: SolveRequest):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Solve this algorithm problem in {request.language}:\n\n{request.problem}"},
        ]
        async for chunk in self.client.chat_stream(messages):
            yield chunk

    async def _full_solve(self, request: SolveRequest) -> SolveResponse:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Solve this algorithm problem in {request.language}:\n\n{request.problem}"},
        ]
        result = await self.client.structured_output(messages, schema={})
        solution = Solution(**result)
        test_cases = solution.test_cases

        benchmarks = []
        if test_cases:
            exec_results = execute_code(solution.code, request.language, test_cases)
            passed = sum(1 for r in exec_results if r["passed"])
            benchmarks.append(BenchmarkResult(
                language=request.language,
                time_ms=0.0,
                memory_mb=0.0,
                test_cases_passed=passed,
                test_cases_total=len(test_cases),
            ))

        return SolveResponse(
            solution=solution,
            benchmarks=benchmarks,
            tokens_used=self.client.total_tokens,
            model=self.client.model,
        )

    async def _get_hints(self, request: SolveRequest) -> SolveResponse:
        messages = [
            {"role": "system", "content": HINT_PROMPT},
            {"role": "user", "content": f"Give me progressive hints for this problem:\n\n{request.problem}"},
        ]
        result = await self.client.structured_output(messages, schema={})
        hints = result.get("hints", [])
        insight = result.get("key_insight", "")
        explanation = "Progressive Hints:\n\n"
        for i, h in enumerate(hints, 1):
            explanation += f"Hint {i}: {h}\n\n"
        explanation += f"\nKey Insight: {insight}"

        solution = Solution(
            approach="Hints",
            language=request.language,
            code="",
            complexity_time="N/A",
            complexity_space="N/A",
            explanation=explanation,
            test_cases=[],
        )
        return SolveResponse(
            solution=solution,
            tokens_used=self.client.total_tokens,
            model=self.client.model,
        )
