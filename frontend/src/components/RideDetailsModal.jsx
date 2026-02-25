import { useState } from "react";
import { Modal, Box, Typography, Button, Stack } from "@mui/material";
import { motion } from "framer-motion";
import api from "../api/axios";
import ParticipantsModal from "./ParticipantsModal";

export default function RideDetailsModal({ ride, onClose, currentUser }) {
  const [participantsOpen, setParticipantsOpen] = useState(false);
  const [rideState, setRideState] = useState(ride); // local copy to update status

  // Guard against undefined ride or missing data
  if (!rideState || !rideState.host || !rideState.participants) {
    return null;
  }

  const isHost = currentUser && rideState.host.userId === currentUser.userId;
  const participant = currentUser && rideState.participants.approved?.find(
    (p) => p.userId === currentUser.userId
  );

  const handleJoin = async () => {
    try {
      await api.post(`/rides/${rideState.rideId}/request`);
      alert("Join request sent!");
    } catch (err) {
      alert(err.response?.data?.detail || "Error sending join request");
    }
  };

  const handleLeave = async () => {
    try {
      await api.post(`/rides/${rideState.rideId}/leave`);
      alert("You left the ride");
    } catch (err) {
      alert(err.response?.data?.detail || "Error leaving ride");
    }
  };

  const handleCancel = async () => {
    try {
      await api.patch(`/rides/${rideState.rideId}/cancel`);
      alert("Ride canceled");
      onClose();
    } catch (err) {
      alert(err.response?.data?.detail || "Error canceling ride");
    }
  };

  return (
    <>
      <Modal open onClose={onClose}>
        <Box
          component={motion.div}
          initial={{ y: "100%" }}
          animate={{ y: 0 }}
          exit={{ y: "100%" }}
          sx={{
            position: "absolute",
            bottom: 0,
            width: "100%",
            maxHeight: "80%",
            bgcolor: "background.paper",
            borderRadius: 3,
            p: 3,
            overflowY: "auto",
            outline: "none",
          }}
        >
          <Typography variant="h4" fontWeight="bold">
            {rideState.rideName}
          </Typography>
          <Typography mt={1}>
            {rideState.rideStartPoint} → {rideState.rideEndPoint}
          </Typography>
          <Typography>
            Start Time: {new Date(rideState.rideStartTime).toLocaleString()}
          </Typography>
          {rideState.rideDuration && (
            <Typography>Duration: {rideState.rideDuration} hrs</Typography>
          )}
          {rideState.haltDuration && (
            <Typography>Halt: {rideState.haltDuration} hrs</Typography>
          )}
          <Typography>Status: {rideState.status}</Typography>
          <Typography>Host: {rideState.host.username}</Typography>

          <Stack direction="row" spacing={2} mt={3}>
            {!participant && !isHost && (
              <Button variant="contained" onClick={handleJoin}>
                Join Ride
              </Button>
            )}
            {participant && !isHost && (
              <Button variant="outlined" color="error" onClick={handleLeave}>
                Leave Ride
              </Button>
            )}
            {isHost && (
              <Button variant="contained" color="error" onClick={handleCancel}>
                Cancel Ride
              </Button>
            )}
            <Button
              variant="outlined"
              onClick={() => setParticipantsOpen(true)}
            >
              Participants
            </Button>
          </Stack>

          <Button
            variant="text"
            sx={{ mt: 3 }}
            onClick={onClose}
          >
            Close
          </Button>
        </Box>
      </Modal>

      {participantsOpen && (
        <ParticipantsModal
          ride={rideState}
          onClose={() => setParticipantsOpen(false)}
          currentUser={currentUser}
        />
      )}
    </>
  );
}
