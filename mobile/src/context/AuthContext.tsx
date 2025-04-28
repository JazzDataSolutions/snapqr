// src/contexts/AuthContext.tsx
import React, { createContext, useState, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { login as apiLogin } from "../infrastructure/api/authApi";

export const AuthContext = createContext<any>(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    AsyncStorage.getItem("token").then(t => setToken(t));
  }, []);

  const login = async (email:string, password:string) => {
    const { accessToken } = await apiLogin(email, password);
    await AsyncStorage.setItem("token", accessToken);
    setToken(accessToken);
  };

  return (
    <AuthContext.Provider value={{ token, login }}>
      {children}
    </AuthContext.Provider>
  );
}

