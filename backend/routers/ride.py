from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.ride import Ride
from services.ride import create_ride as ride_service_create
from db.dependencies import get_db
from routers.auth import get_current_user
from services.ride import get_all_rides, get_upcoming_rides
import uuid
from services.ride import request_ride_participation, decide_participation
from typing import List
from services.ride import get_ride_details, leave_ride, cancel_ride
from db.models import User


router = APIRouter(tags=["rides"])

#-----------------------------------------------------------
# create a new ride using the currently authenticated user
#-----------------------------------------------------------
@router.post("/rides")
def create_ride(ride: Ride,db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
        try:
            new_ride = ride_service_create(
                db=db,
                ride_data=ride,
                host_id=current_user.userId  # pass current user ID
            )
            return new_ride
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

# -------------------------
# Get all rides
# -------------------------
@router.get("/rides", response_model=List[Ride])
def show_all_rides(db: Session = Depends(get_db)):
    rides = get_all_rides(db)
    return rides


# -------------------------
# Get UPCOMING rides
# -------------------------
@router.get("/rides/upcoming", response_model=List[Ride])
def show_upcoming_rides(db: Session = Depends(get_db)):
    rides = get_upcoming_rides(db)
    return rides

# ----------------------------
# join ride(request the host)
# ----------------------------
@router.post("/rides/{ride_id}/request")
def request_participation(
    ride_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        participation = request_ride_participation(
            db=db,
            user_id=current_user.userId,
            ride_id=ride_id,
        )
        return participation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# -------------------------------
# approve ride(done by the host)
# -------------------------------
@router.post("/rides/{ride_id}/participants/{user_id}/decision")
def decide_participant_route(
    ride_id: str,
    user_id: str,
    approve: bool, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        result = decide_participation(
            db=db,
            host_id=current_user.userId,
            ride_id=ride_id,
            participant_user_id=user_id,
            approve=approve
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )




# --------------------------------
# get all details about the ride
# --------------------------------
@router.get("/rides/{ride_id}")
def read_ride_details(
    ride_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_ride_details(
        db=db,
        ride_id=ride_id,
        requester_id=current_user.userId
    )


# --------------------------------
# leave ride(for participant)
# --------------------------------
@router.delete("/rides/{ride_id}/leave")
def leave_ride_route(
    ride_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return leave_ride(db, ride_id, current_user.userId)


# ------------------------------------------------
# cancel ride(only for the host)
# ------------------------------------------------
@router.patch("/rides/{ride_id}/cancel")
def cancel_ride_route(
    ride_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return cancel_ride(db, ride_id, current_user.userId)
