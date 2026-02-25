import { useState, useContext } from "react";
import { Box, TextField, Button, Typography, Stack } from "@mui/material";
import api from "../api/axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const { setToken, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [bikeName, setBikeName] = useState("");
  const [age, setAge] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await api.post("/signup", {
        name,
        username,
        password,
        bikeName,
        age: parseInt(age, 10),
      });
      const jwt = res.data.access_token;

      localStorage.setItem("token", jwt);
      setToken(jwt);

      // Optionally fetch user profile
      const userRes = await api.get("/users/me", {
        headers: { Authorization: `Bearer ${jwt}` },
      });
      setCurrentUser(userRes.data);

      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed");
      console.error(err);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        maxWidth: 400,
        mx: "auto",
        mt: 10,
        p: 4,
        borderRadius: 3,
        boxShadow: 3,
        bgcolor: "background.paper",
      }}
    >
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Sign Up
      </Typography>
      <Stack spacing={2}>
        <TextField
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <TextField
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <TextField
          label="Bike Name"
          value={bikeName}
          onChange={(e) => setBikeName(e.target.value)}
          required
        />
        <TextField
          label="Age"
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
        />

        {error && (
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        )}

        <Button variant="contained" type="submit">
          Sign Up
        </Button>
      </Stack>
    </Box>
  );
}
