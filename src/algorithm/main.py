"""FastAPI entry point for orbit-algo-mind."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .models import SolveRequest, SolveResponse
from .agent import AlgorithmAgent

app = FastAPI(title="orbit-algo-mind", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

agent = AlgorithmAgent()


@app.get("/health")
async def health():
    return {"status": "ok", "mock_mode": agent.client.mock_mode}


@app.post("/api/solve")
async def solve(request: SolveRequest):
    result = await agent.solve(request)
    return result


@app.post("/api/solve/stream")
async def solve_stream(request: SolveRequest):
    return StreamingResponse(agent.solve_stream(request), media_type="text/event-stream")


@app.get("/api/stats")
async def stats():
    return agent.client.get_usage_stats()
