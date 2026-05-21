"use client";

import { useState } from "react";

interface TestCase {
  input: string;
  expected: string;
  description?: string;
}

interface Benchmark {
  language: string;
  time_ms: number;
  test_cases_passed: number;
  test_cases_total: number;
}

interface SolutionData {
  solution: {
    approach: string;
    language: string;
    code: string;
    complexity_time: string;
    complexity_space: string;
    explanation: string;
    test_cases: TestCase[];
  };
  benchmarks: Benchmark[];
}

function CodeBlock({ code, language }: { code: string; language: string }) {
  const keywords: Record<string, string[]> = {
    python: ["def", "class", "return", "if", "else", "elif", "for", "while", "in", "not", "and", "or", "True", "False", "None", "import", "from", "print", "range", "len", "append", "self"],
    cpp: ["int", "string", "vector", "auto", "return", "if", "else", "for", "while", "class", "public", "private", "void", "bool", "map", "set", "pair", "#include", "using", "namespace", "std", "cout", "endl"],
    go: ["func", "package", "import", "return", "if", "else", "for", "range", "var", "const", "type", "struct", "map", "int", "string", "bool", "fmt", "make", "len"],
  };

  const kws = keywords[language] || [];
  const highlighted = code.split("\n").map((line, i) => {
    let html = line
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Strings
    html = html.replace(/(["'`])(?:(?!\1)[^\\]|\\.)*\1/g, '<span style="color:#a5d6ff">$&</span>');
    // Comments
    html = html.replace(/(#.*|\/\/.*|\/\*[\s\S]*?\*\/)/g, '<span style="color:#8b949e">$&</span>');
    // Numbers
    html = html.replace(/\b(\d+\.?\d*)\b/g, '<span style="color:#79c0ff">$1</span>');
    // Keywords
    for (const kw of kws) {
      const re = new RegExp(`\\b(${kw})\\b`, "g");
      html = html.replace(re, '<span style="color:#ff7b72">$1</span>');
    }

    return (
      <div key={i} style={{ display: "flex" }}>
        <span style={{ width: "3rem", textAlign: "right", paddingRight: "1rem", color: "#484f58", userSelect: "none" }}>
          {i + 1}
        </span>
        <span dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    );
  });

  return (
    <pre style={{
      margin: 0,
      padding: "1rem",
      fontSize: "0.85rem",
      lineHeight: 1.6,
      overflow: "auto",
      background: "#0d1117",
      borderRadius: 6,
    }}>
      {highlighted}
    </pre>
  );
}

export function SolutionView({ data }: { data: SolutionData }) {
  const [activeTab, setActiveTab] = useState<"code" | "tests">("code");
  if (!data) return null;
  const { solution, benchmarks } = data;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      {/* Approach & Complexity */}
      <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8 }}>
        <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
          <span style={{ padding: "0.2rem 0.8rem", background: "#8b5cf6", color: "white", borderRadius: 4, fontSize: "0.85rem", fontWeight: "bold" }}>
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
        <p style={{ margin: 0, color: "#ccc", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>{solution.explanation}</p>
      </div>

      {/* Code & Tests tabs */}
      <div style={{ background: "#1a1a1a", border: "1px solid #333", borderRadius: 8, overflow: "hidden" }}>
        <div style={{ display: "flex", borderBottom: "1px solid #333" }}>
          <button
            onClick={() => setActiveTab("code")}
            style={{
              padding: "0.6rem 1.5rem",
              background: activeTab === "code" ? "#0d1117" : "transparent",
              color: activeTab === "code" ? "#e0e0e0" : "#888",
              border: "none",
              borderBottom: activeTab === "code" ? "2px solid #3b82f6" : "2px solid transparent",
              cursor: "pointer",
              fontSize: "0.9rem",
            }}
          >
            Solution Code
          </button>
          <button
            onClick={() => setActiveTab("tests")}
            style={{
              padding: "0.6rem 1.5rem",
              background: activeTab === "tests" ? "#0d1117" : "transparent",
              color: activeTab === "tests" ? "#e0e0e0" : "#888",
              border: "none",
              borderBottom: activeTab === "tests" ? "2px solid #3b82f6" : "2px solid transparent",
              cursor: "pointer",
              fontSize: "0.9rem",
            }}
          >
            Test Cases ({solution.test_cases?.length || 0})
          </button>
        </div>

        <div style={{ padding: "1rem" }}>
          {activeTab === "code" && solution.code && (
            <CodeBlock code={solution.code} language={solution.language} />
          )}
          {activeTab === "tests" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {solution.test_cases?.map((tc, i) => (
                <div key={i} style={{ padding: "0.75rem", background: "#0d1117", borderRadius: 4, fontFamily: "monospace", fontSize: "0.8rem" }}>
                  <div><strong>Input:</strong> <span style={{ color: "#79c0ff" }}>{tc.input}</span></div>
                  <div><strong>Expected:</strong> <span style={{ color: "#7ee787" }}>{tc.expected}</span></div>
                  {tc.description && <div style={{ color: "#888", marginTop: "0.25rem" }}>{tc.description}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Benchmarks */}
      {benchmarks?.length > 0 && (
        <div style={{ padding: "1.5rem", background: "#1a1a1a", border: "1px solid #333", borderRadius: 8 }}>
          <h3 style={{ margin: "0 0 1rem", color: "#e0e0e0" }}>Execution Results</h3>
          {benchmarks.map((b, i) => (
            <div key={i} style={{ display: "flex", gap: "1rem", alignItems: "center", flexWrap: "wrap" }}>
              <span style={{ padding: "0.2rem 0.6rem", background: "#333", borderRadius: 4, fontSize: "0.85rem" }}>{b.language}</span>
              <span style={{
                padding: "0.2rem 0.6rem",
                background: b.test_cases_passed === b.test_cases_total ? "#166534" : "#7f1d1d",
                color: b.test_cases_passed === b.test_cases_total ? "#86efac" : "#fca5a5",
                borderRadius: 4,
                fontSize: "0.85rem",
                fontWeight: "bold",
              }}>
                {b.test_cases_passed}/{b.test_cases_total} passed
              </span>
              {b.time_ms > 0 && (
                <span style={{ color: "#888", fontSize: "0.8rem" }}>{b.time_ms.toFixed(1)}ms</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
