import { useState, useContext } from "react";
import { Box, TextField, Button, Typography, Stack } from "@mui/material";
import api from "../api/axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { setToken, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  try {
    // this code has been changed to use the URLSearchParams for x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    const res = await api.post("/token", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    console.log(res.data); // <--- check this

    const jwt = res.data.access_token;

    localStorage.setItem("token", jwt);
    console.log("..........");
    setToken(jwt);


    // Optionally fetch user profile
    const userRes = await api.get("/users/me", {
      headers: { Authorization: `Bearer ${jwt}` },
    });

    setCurrentUser(userRes.data);

    navigate("/dashboard");

  } catch (err) {
    console.log(err)
    setError(err.response?.data?.detail || "Login failed");
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
        Login
      </Typography>
      <Stack spacing={2}>
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

        {error && (
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        )}

        <Button variant="contained" type="submit">
          Login
        </Button>
      </Stack>
    </Box>
  );
}
