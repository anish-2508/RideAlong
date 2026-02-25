import { createContext, useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "./AuthContext";

export const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
  const { token } = useContext(AuthContext);
  const wsRef = useRef(null);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (!token) return;

    const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received:", data);
        setNotifications((prev) => [data, ...prev]);
        // Optionally: use browser notification
        if (Notification.permission === "granted") {
          new Notification("Ride Notification", { body: JSON.stringify(data) });
        }
      } catch (err) {
        console.error("WS parse error:", err);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected, reconnecting in 2s...");
      setTimeout(() => {
        if (token) wsRef.current = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
      }, 2000);
    };

    return () => ws.close();
  }, [token]);

  const sendMessage = (message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return (
    <WebSocketContext.Provider value={{ notifications, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
};
