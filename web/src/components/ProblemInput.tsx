"use client";

import { useState } from "react";

export function ProblemInput({ onSubmit, loading }: { onSubmit: (problem: string) => void; loading: boolean }) {
  const [problem, setProblem] = useState("");

  return (
    <div style={{ marginBottom: "2rem" }}>
      <textarea
        value={problem}
        onChange={(e) => setProblem(e.target.value)}
        placeholder={"Paste your algorithm problem here...\n\nExample:\nGiven an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."}
        rows={12}
        style={{
          width: "100%",
          padding: "1rem",
          background: "#1a1a1a",
          color: "#e0e0e0",
          border: "1px solid #333",
          borderRadius: 6,
          fontFamily: "monospace",
          fontSize: "0.9rem",
          resize: "vertical",
          boxSizing: "border-box",
        }}
      />
      <button
        onClick={() => onSubmit(problem)}
        disabled={loading || !problem.trim()}
        style={{
          marginTop: "0.5rem",
          padding: "0.6rem 2rem",
          background: loading ? "#555" : "#8b5cf6",
          color: "white",
          border: "none",
          borderRadius: 6,
          cursor: loading ? "not-allowed" : "pointer",
          fontSize: "1rem",
        }}
      >
        {loading ? "Solving..." : "Solve Problem"}
      </button>
    </div>
  );
}
