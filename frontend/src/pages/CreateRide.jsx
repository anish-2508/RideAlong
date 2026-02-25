import { useState, useContext } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Stack,
} from "@mui/material";
import { DateTimePicker } from "@mui/lab";
import { LocalizationProvider } from "@mui/lab";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import api from "../api/axios";
import { AuthContext } from "../context/AuthContext";

export default function CreateRide() {
  const { token } = useContext(AuthContext);

  const [rideName, setRideName] = useState("");
  const [startPoint, setStartPoint] = useState("");
  const [endPoint, setEndPoint] = useState("");
  const [startTime, setStartTime] = useState(new Date());
  const [rideDuration, setRideDuration] = useState("");
  const [haltDuration, setHaltDuration] = useState("");
  const [maxParticipants, setMaxParticipants] = useState(20);
  const [routeLink, setRouteLink] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post(
        "/create-ride",
        {
          rideName,
          rideStartTime: startTime.toISOString(),
          rideStartPoint: startPoint,
          rideEndPoint: endPoint,
          rideDuration: rideDuration || null,
          haltDuration: haltDuration || null,
          maxParticipants,
          routeLink,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Ride created successfully!");
      // Optionally, redirect or reset form
    } catch (err) {
      alert(err.response?.data?.detail || "Error creating ride");
      console.error(err);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        maxWidth: 500,
        mx: "auto",
        mt: 5,
        p: 3,
        borderRadius: 3,
        boxShadow: 3,
        bgcolor: "background.paper",
      }}
    >
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Create Ride
      </Typography>
      <Stack spacing={2}>
        <TextField
          label="Ride Name"
          value={rideName}
          onChange={(e) => setRideName(e.target.value)}
          required
        />
        <TextField
          label="Start Point"
          value={startPoint}
          onChange={(e) => setStartPoint(e.target.value)}
          required
        />
        <TextField
          label="End Point"
          value={endPoint}
          onChange={(e) => setEndPoint(e.target.value)}
          required
        />
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DateTimePicker
            label="Start Time"
            value={startTime}
            onChange={setStartTime}
            renderInput={(props) => <TextField {...props} required />}
          />
        </LocalizationProvider>
        <TextField
          label="Ride Duration (hrs)"
          type="number"
          value={rideDuration}
          onChange={(e) => setRideDuration(e.target.value)}
        />
        <TextField
          label="Halt Duration (hrs)"
          type="number"
          value={haltDuration}
          onChange={(e) => setHaltDuration(e.target.value)}
        />
        <TextField
          label="Max Participants"
          type="number"
          value={maxParticipants}
          onChange={(e) => setMaxParticipants(e.target.value)}
          required
        />
        <TextField
          label="Route Link"
          value={routeLink}
          onChange={(e) => setRouteLink(e.target.value)}
        />

        <Button variant="contained" type="submit">
          Create Ride
        </Button>
      </Stack>
    </Box>
  );
}
