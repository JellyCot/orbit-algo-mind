"use client";

export function SolutionView({ data }: { data: any }) {
  if (!data) return null;
  const { solution, benchmarks } = data;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      {/* Approach & Complexity */}
      <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8 }}>
        <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
          <span style={{ padding: "0.2rem 0.8rem", background: "#8b5cf6", color: "white", borderRadius: 4, fontSize: "0.85rem" }}>
            {solution.approach}
          </span>
          <span style={{ padding: "0.2rem 0.8rem", background: "#333", color: "#aaa", borderRadius: 4, fontSize: "0.85rem" }}>
            {solution.language}
          </span>
          <span style={{ padding: "0.2rem 0.8rem", background: "#166534", color: "#86efac", borderRadius: 4, fontSize: "0.85rem" }}>
            Time: {solution.complexity_time}
          </span>
          <span style={{ padding: "0.2rem 0.8rem", background: "#1e3a5f", color: "#93c5fd", borderRadius: 4, fontSize: "0.85rem" }}>
            Space: {solution.complexity_space}
          </span>
        </div>
        <p style={{ margin: 0, color: "#ccc", lineHeight: 1.6 }}>{solution.explanation}</p>
      </div>

      {/* Code */}
      {solution.code && (
        <div style={{ padding: "1.5rem", background: "#0d1117", border: "1px solid #333", borderRadius: 8 }}>
          <h3 style={{ margin: "0 0 1rem", color: "#e0e0e0" }}>Solution</h3>
          <pre style={{ margin: 0, fontSize: "0.85rem", lineHeight: 1.5, overflow: "auto" }}>
            <code>{solution.code}</code>
          </pre>
        </div>
      )}

      {/* Test Cases */}
      {solution.test_cases?.length > 0 && (
        <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8 }}>
          <h3 style={{ margin: "0 0 1rem", color: "#e0e0e0" }}>Test Cases ({solution.test_cases.length})</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            {solution.test_cases.map((tc: any, i: number) => (
              <div key={i} style={{ padding: "0.75rem", background: "#0d1117", borderRadius: 4, fontFamily: "monospace", fontSize: "0.8rem" }}>
                <div><strong>Input:</strong> {tc.input}</div>
                <div><strong>Expected:</strong> {tc.expected}</div>
                {tc.description && <div style={{ color: "#888" }}>{tc.description}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Benchmarks */}
      {benchmarks?.length > 0 && (
        <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8 }}>
          <h3 style={{ margin: "0 0 1rem", color: "#e0e0e0" }}>Test Results</h3>
          {benchmarks.map((b: any, i: number) => (
            <div key={i} style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
              <span style={{ color: "#aaa" }}>{b.language}</span>
              <span style={{ color: b.test_cases_passed === b.test_cases_total ? "#22c55e" : "#ef4444" }}>
                {b.test_cases_passed}/{b.test_cases_total} passed
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
