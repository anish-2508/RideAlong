import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

// MUI custom theme
const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#006400", // dark green
    },
    secondary: {
      main: "#f5f5dc", // beige
    },
    background: {
      default: "#f0f0f0",
      paper: "#ffffff",
    },
  },
  typography: {
    fontFamily: "'Roboto', sans-serif",
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
