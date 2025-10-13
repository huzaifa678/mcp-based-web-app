import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CodeUploader from "./pages/main";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CodeUploader />} />
      </Routes>
    </Router>
  );
}

export default App;
