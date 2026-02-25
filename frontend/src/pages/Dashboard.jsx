import { useState, useEffect, useContext } from "react";
import { Box, Tabs, Tab, CircularProgress, Typography, Stack, Fab } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RideCard from "../components/RideCard";
import api from "../api/axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const { token, currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [tab, setTab] = useState(0);
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch user data if token exists but currentUser is not loaded
  useEffect(() => {
    if (token && !currentUser) {
      const fetchUserData = async () => {
        try {
          const res = await api.get("/users/me", {
            headers: { Authorization: `Bearer ${token}` },
          });
          setCurrentUser(res.data);
        } catch (err) {
          console.error("Error fetching user data:", err);
          // Redirect to login if token is invalid
          navigate("/login");
        }
      };
      fetchUserData();
    }
  }, [token, currentUser, setCurrentUser, navigate]);

  const fetchRides = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/rides", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setRides(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error fetching rides");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRides();
  }, []);

  const filteredRides = () => {
    if (!currentUser) return [];
    switch (tab) {
      case 1: // Hosted
        return rides.filter((r) => r.host.userId === currentUser.userId);
      case 2: // Participating
        return rides.filter((r) =>
          r.participants.approved?.some((p) => p.userId === currentUser.userId)
        );
      case 3: // Available (upcoming, not host, not participating)
        return rides.filter(
          (r) =>
            r.status === "UPCOMING" &&
            r.host.userId !== currentUser.userId &&
            !r.participants.approved?.some((p) => p.userId === currentUser.userId)
        );
      default:
        return rides;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {loading && (
        <Box textAlign="center" mt={5}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Typography color="error" mt={2}>
          {error}
        </Typography>
      )}

      {!loading && !error && !currentUser && (
        <Typography mt={2}>Loading user data...</Typography>
      )}

      {!loading && !error && currentUser && (
        <>
          <Tabs
            value={tab}
            onChange={(e, val) => setTab(val)}
            sx={{ mb: 3 }}
          >
            <Tab label="All" />
            <Tab label="Hosted" />
            <Tab label="Participating" />
            <Tab label="Available" />
          </Tabs>

          <Stack spacing={2}>
            {filteredRides().length > 0 ? (
              filteredRides().map((ride) => (
                <RideCard key={ride.rideId} ride={ride} currentUser={currentUser} />
              ))
            ) : (
              <Typography>No rides found.</Typography>
            )}
          </Stack>
        </>
      )}

      <Fab
        color="primary"
        aria-label="create ride"
        onClick={() => navigate("/create-ride")}
        sx={{ position: "fixed", bottom: 16, right: 16 }}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
}
