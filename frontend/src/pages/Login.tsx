import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { redirect } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      await login(username, password);
      alert("Logged in!");
      navigate("/");
    } catch (err) {
      setError("Login failed");
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="border p-2 w-full mb-2"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="border p-2 w-full mb-2"
      />
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <button onClick={handleLogin} className="bg-blue-500 text-white p-2 w-full">
        Login
      </button>
      <button
        onClick={() => (window.location.href = "/register")}
        className="mt-2 bg-gray-500 text-white p-2 w-full"
      >
        Register
      </button>
    </div>
  );
};
