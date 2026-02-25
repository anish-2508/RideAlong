// context/AuthContext.jsx
import { createContext, useState } from "react";

export const AuthContext = createContext({});

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [currentUser, setCurrentUser] = useState(null);

  return (
    <AuthContext.Provider value={{ token, setToken, currentUser, setCurrentUser }}>
      {children}
    </AuthContext.Provider>
  );
}
