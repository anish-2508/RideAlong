import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { WebSocketProvider } from "./context/WebSocketContext";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import CreateRide from "./pages/CreateRide";
import RideDetailsModal from "./components/RideDetailsModal";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/login" />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <WebSocketProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/create-ride"
              element={
                <ProtectedRoute>
                  <CreateRide />
                </ProtectedRoute>
              }
            />

            <Route
              path="/rides/:rideId"
              element={
                <ProtectedRoute>
                  <RideDetailsModal />
                </ProtectedRoute>
              }
            />

            <Route path="*" element={<Navigate to="/dashboard" />} />
          </Routes>
        </Router>
      </WebSocketProvider>
    </AuthProvider>
  );
}
