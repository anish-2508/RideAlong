import { useState } from "react";
import { Paper, Typography, Box } from "@mui/material";
import { motion } from "framer-motion";
import RideDetailsModal from "./RideDetailsModal";

export default function RideCard({ ride, currentUser }) {
  const [open, setOpen] = useState(false);

  // Guard against undefined ride or missing host
  if (!ride || !ride.host) {
    return null;
  }

  return (
    <>
      <Paper
        component={motion.div}
        elevation={4}
        sx={{
          p: 2,
          cursor: "pointer",
          "&:hover": { transform: "scale(1.03)" },
          transition: "transform 0.2s",
        }}
        onClick={() => setOpen(true)}
      >
        <Typography variant="h6" fontWeight="bold">
          {ride.rideName}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {ride.rideStartPoint} → {ride.rideEndPoint}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {new Date(ride.rideStartTime).toLocaleString()}
        </Typography>
        <Box mt={1}>
          <Typography variant="caption" color="text.secondary">
            Host: {ride.host.username}
          </Typography>
        </Box>
      </Paper>

      {open && (
        <RideDetailsModal
          ride={ride}
          onClose={() => setOpen(false)}
          currentUser={currentUser}
        />
      )}
    </>
  );
}
