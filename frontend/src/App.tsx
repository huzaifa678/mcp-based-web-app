import React, { JSX } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import CodeUploader from "./pages/Main";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { LoginPage } from "./pages/Login";
import { RegisterPage } from "./pages/Register";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { accessToken, loading } = useAuth();

  if (loading) return <div>Loading...</div>; 
  if (!accessToken) return <Navigate to="/login" replace />;

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <CodeUploader />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
