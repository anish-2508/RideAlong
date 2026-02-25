from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

# User schema for responses
class UserResponse(BaseModel):
    userId: str
    username: str
    
    class Config:
        from_attributes = True

# Participant info in ride responses
class ParticipantInfo(BaseModel):
    userId: str
    username: str
    status: str
    
    class Config:
        from_attributes = True

class ParticipantsGroup(BaseModel):
    approved: List[ParticipantInfo] = []
    pending: List[ParticipantInfo] = []
    rejected: List[ParticipantInfo] = []

# Request model for creating rides
class Ride(BaseModel):
    rideName: str
    rideStartTime: datetime
    rideStartPoint: str
    rideEndPoint: str
    rideDuration: Optional[float] = None
    haltDuration: Optional[float] = None
    routeLink: Optional[str] = None
    maxParticipants: int = 20

# Response model for listing rides
class RideResponse(BaseModel):
    rideId: str
    rideName: str
    rideStartTime: datetime
    rideStartPoint: str
    rideEndPoint: str
    rideDuration: Optional[float] = None
    haltDuration: Optional[float] = None
    routeLink: Optional[str] = None
    maxParticipants: int
    status: str
    host: UserResponse
    participants: ParticipantsGroup
    
    class Config:
        from_attributes = True


