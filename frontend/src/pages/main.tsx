import React, { useState } from "react";
import { analyzeCode } from "../api/mcpClient";

export default function CodeUploader() {
  const [code, setCode] = useState("");
  const [feedback, setFeedback] = useState<any>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => setCode(reader.result as string);
      reader.readAsText(file);
    }
  };

  const handleAnalyze = async () => {
    const res = await analyzeCode(code);
    setFeedback(res);
  };

  return (
    <div>
      <input type="file" accept=".py" onChange={handleFileUpload} />
      <button onClick={handleAnalyze}>Analyze Code</button>

      {feedback && (
        <div>
          {feedback.static?.map((f: any, i: number) => (
            <p key={i}>🔹 {f.message}</p>
          ))}
          {feedback.ai?.map((f: any, i: number) => (
            <p key={i}>💡 {f.message}</p>
          ))}
        </div>
      )}
    </div>
  );
}
