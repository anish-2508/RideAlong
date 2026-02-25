import { Modal, Box, Typography, Button, List, ListItem, ListItemText, Divider } from "@mui/material";
import { motion } from "framer-motion";
import { useState } from "react";
import api from "../api/axios";

export default function ParticipantsModal({ ride, onClose, currentUser }) {
  const [participants, setParticipants] = useState(ride?.participants || {});

  // Guard against undefined ride or missing data
  if (!ride || !ride.host) {
    return null;
  }
  
  const handleDecision = async (userId, approve) => {
    try {
      await api.post(`/rides/${ride.rideId}/participants/${userId}/decision`, null, {
        params: { approve }
      });
      setParticipants((prev) => {
        const updated = { ...prev };
        // Move participant to approved/rejected
        const index = updated.pending.findIndex(p => p.userId === userId);
        if (index !== -1) {
          const [p] = updated.pending.splice(index, 1);
          p.status = approve ? "APPROVED" : "REJECTED";
          if (approve) updated.approved.push(p);
          else updated.rejected.push(p);
        }
        return { ...updated };
      });
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Error updating participant");
    }
  };

  const isHost = currentUser && ride.host.userId === currentUser.userId;

  return (
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
          maxHeight: "70%",
          bgcolor: "background.paper",
          borderRadius: 3,
          p: 3,
          overflowY: "auto",
          outline: "none",
        }}
      >
        <Typography variant="h5" fontWeight="bold" mb={2}>
          Participants
        </Typography>

        <Typography variant="subtitle1" fontWeight="bold">Approved</Typography>
        <List dense>
          {participants.approved?.map(p => (
            <ListItem key={p.userId}>
              <ListItemText primary={p.username} />
            </ListItem>
          ))}
        </List>

        {isHost && (
          <>
            <Divider sx={{ my: 1 }} />
            <Typography variant="subtitle1" fontWeight="bold">Pending</Typography>
            <List dense>
              {participants.pending?.map(p => (
                <ListItem key={p.userId} secondaryAction={
                  <>
                    <Button size="small" onClick={() => handleDecision(p.userId, true)}>Approve</Button>
                    <Button size="small" onClick={() => handleDecision(p.userId, false)}>Reject</Button>
                  </>
                }>
                  <ListItemText primary={p.username} />
                </ListItem>
              ))}
            </List>
          </>
        )}

        <Divider sx={{ my: 1 }} />
        <Typography variant="subtitle1" fontWeight="bold">Rejected</Typography>
        <List dense>
          {participants.rejected?.map(p => (
            <ListItem key={p.userId}>
              <ListItemText primary={p.username} />
            </ListItem>
          ))}
        </List>

        <Button
          variant="contained"
          sx={{ mt: 3 }}
          onClick={onClose}
        >
          Close
        </Button>
      </Box>
    </Modal>
  );
}
