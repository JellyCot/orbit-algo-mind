"use client";

import { useState } from "react";
import { ProblemInput } from "@/components/ProblemInput";
import { SolutionView } from "@/components/SolutionView";

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState("");
  const [language, setLanguage] = useState("python");
  const [mode, setMode] = useState<"full" | "hints">("full");

  const handleSolve = async (problem: string) => {
    setLoading(true);
    setResult(null);
    setStreaming("");

    const resp = await fetch("/api/solve/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problem, language, mode }),
    });
    const reader = resp.body?.getReader();
    const decoder = new TextDecoder();
    let text = "";
    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
      setStreaming(text);
    }

    // Also get structured result
    const syncResp = await fetch("/api/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problem, language, mode }),
    });
    const data = await syncResp.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main style={{ maxWidth: 1200, margin: "0 auto", padding: "2rem" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>orbit-algo-mind</h1>
      <p style={{ color: "#888", marginBottom: "2rem" }}>
        AI algorithm solving and teaching agent — paste a problem, get solutions in multiple languages.
      </p>

      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          style={{ padding: "0.4rem", background: "#1a1a1a", color: "#e0e0e0", border: "1px solid #333", borderRadius: 6 }}
        >
          <option value="python">Python</option>
          <option value="cpp">C++</option>
          <option value="go">Go</option>
        </select>
        <button
          onClick={() => setMode("full")}
          style={{ padding: "0.4rem 1rem", background: mode === "full" ? "#3b82f6" : "#333", color: "white", border: "none", borderRadius: 6, cursor: "pointer" }}
        >
          Full Solution
        </button>
        <button
          onClick={() => setMode("hints")}
          style={{ padding: "0.4rem 1rem", background: mode === "hints" ? "#3b82f6" : "#333", color: "white", border: "none", borderRadius: 6, cursor: "pointer" }}
        >
          Progressive Hints
        </button>
      </div>

      <ProblemInput onSubmit={handleSolve} loading={loading} />

      {streaming && !result && (
        <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8, whiteSpace: "pre-wrap", fontFamily: "monospace", fontSize: "0.85rem" }}>
          {streaming}
        </div>
      )}
      {result && <SolutionView data={result} />}
    </main>
  );
}
