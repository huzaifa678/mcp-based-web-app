import React, { createContext, useState, useContext, ReactNode, useEffect } from "react";
import axios from "axios";

interface AuthContextType {
  user: string | null;
  accessToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_URL = "/api"; // MCP backend URL

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshTokenValue, setRefreshTokenValue] = useState<string | null>(() =>
    localStorage.getItem("refreshToken")
  );

  useEffect(() => {
  const init = async () => {
    if (refreshTokenValue) {
      await refreshTokenCall();
    }
    setLoading(false);
    };
    init();
  }, [refreshTokenValue]);

  const login = async (username: string, password: string) => {
    const res = await axios.post(`${API_URL}/login`, { username, password });
    setAccessToken(res.data.access_token);
    setRefreshTokenValue(res.data.refresh_token);
    setUser(username);
    localStorage.setItem("refreshToken", res.data.refresh_token);
  };

  const register = async (username: string, password: string) => {
    await axios.post(`${API_URL}/register`, { username, password });
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    setRefreshTokenValue(null);
    localStorage.removeItem("refreshToken");
  };

  const refreshTokenCall = async () => {
    if (!refreshTokenValue) return;
    try {
      const res = await axios.post(`${API_URL}/renew`, { refresh_token: refreshTokenValue });
      setAccessToken(res.data.access_token);
      setRefreshTokenValue(res.data.refresh_token);
      localStorage.setItem("refreshToken", res.data.refresh_token);
    } catch (err) {
      logout();
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, accessToken, login, register, logout, refreshToken: refreshTokenCall, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};

