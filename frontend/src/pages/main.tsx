import React, { useState, useEffect } from "react";
import { analyzeCode } from "../api/mcpClient";

export default function CodeUploader() {
  const [code, setCode] = useState("");
  const [feedback, setFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showStatic, setShowStatic] = useState(true);
  const [showAI, setShowAI] = useState(true);

  useEffect(() => {
    setShowStatic(feedback?.static?.length > 0);
    setShowAI(feedback?.ai?.length > 0);
  }, [feedback]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onloadend = () => {
      if (reader.result) {
        setCode(reader.result.toString());
      }
    };

    reader.onerror = () => {
      alert("Failed to read file!");
      console.error(reader.error);
    };

    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    if (!code.trim()) return alert("Please upload or enter code first!");
    setLoading(true);
    setFeedback(null);
    try {
      const res = await analyzeCode(code);
      setFeedback(res);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Python Code Analyzer</h2>

      <input
        type="file"
        accept=".py"
        onChange={handleFileUpload}
        className="mb-3 p-2 border rounded w-full"
      />
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Or paste your Python code here..."
        className="mb-3 p-2 border rounded w-full h-40 font-mono"
      />

      <button
        onClick={handleAnalyze}
        className="mb-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>

      {feedback && (
        <div className="space-y-4">
          {/* Static Feedback */}
          {feedback.static?.length > 0 && (
            <div className="border p-3 rounded bg-gray-50">
              <div
                className="flex justify-between items-center cursor-pointer mb-2"
                onClick={() => setShowStatic(!showStatic)}
              >
                <h3 className="font-semibold text-gray-700">
                  🔹 Static Feedback ({feedback.static.length})
                </h3>
                <span>{showStatic ? "▼" : "▲"}</span>
              </div>
              {showStatic &&
                feedback.static.map((f: any, i: number) => (
                  <div
                    key={i}
                    className="flex justify-between items-center p-1 border-b last:border-b-0"
                  >
                    <p className="text-gray-800">{f.message}</p>
                    <button
                      onClick={() => copyToClipboard(f.message)}
                      className="text-sm text-blue-600 hover:underline"
                    >
                      Copy
                    </button>
                  </div>
                ))}
            </div>
          )}

          {/* AI Feedback */}
          {feedback.ai?.length > 0 && (
            <div className="border p-3 rounded bg-yellow-50">
              <div
                className="flex justify-between items-center cursor-pointer mb-2"
                onClick={() => setShowAI(!showAI)}
              >
                <h3 className="font-semibold text-yellow-800">
                  💡 AI Suggestions ({feedback.ai.length})
                </h3>
                <span>{showAI ? "▼" : "▲"}</span>
              </div>
              {showAI &&
                feedback.ai.map((f: any, i: number) => (
                  <div
                    key={i}
                    className="flex justify-between items-center p-1 border-b last:border-b-0"
                  >
                    <p className="text-yellow-900">{f.message}</p>
                    <button
                      onClick={() => copyToClipboard(f.message)}
                      className="text-sm text-yellow-700 hover:underline"
                    >
                      Copy
                    </button>
                  </div>
                ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
