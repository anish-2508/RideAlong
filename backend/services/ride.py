from datetime import datetime, timezone
from db.models import Ride, RideStatus
import uuid
from models.ride import Ride as RideSchema
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime, timezone
from db.models import Ride, RideParticipant, RideStatus, ParticipantStatus
from sqlalchemy import func


#--------------------------
# create a new ride event
#--------------------------
def create_ride(db: Session, host_id: str, ride_data: RideSchema):
    new_ride = Ride(
        rideId=uuid.uuid4(),
        hostId=host_id,
        rideName=ride_data.rideName,
        rideStartTime=ride_data.rideStartTime,
        rideStartPoint=ride_data.rideStartPoint,
        rideEndPoint=ride_data.rideEndPoint,
        rideDuration=ride_data.rideDuration,
        haltDuration=ride_data.haltDuration,
        routeLink=ride_data.routeLink or "",
        maxParticipants=ride_data.maxParticipants,
        status=RideStatus.UPCOMING,
        createdAt=datetime.utcnow()
    )
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride

# -------------------------
# get all rides
# -------------------------
def get_all_rides(db: Session):

    rides = db.query(Ride).options(
        selectinload(Ride.host),
        selectinload(Ride.participants),
    ).all()
    return rides

# -------------------------
# get upcoming rides
# -------------------------
def get_upcoming_rides(db: Session):
    rides = db.query(Ride).filter(
        Ride.status == RideStatus.UPCOMING
    ).options(
        selectinload(Ride.host),
        selectinload(Ride.participants),
    ).all()
    return rides

# ----------------------------
# join ride(request the host)
# ----------------------------
def request_ride_participation( db: Session,user_id: str, ride_id: str):
    stmt = select(Ride).where(Ride.rideId == ride_id)
    ride = db.execute(stmt).scalar_one_or_none()
    if not ride:
        raise ValueError("ride not found")
    if ride.status != RideStatus.UPCOMING:
        raise ValueError("cannot join a ride that is not upcoming")
    if ride.hostId == user_id:
        raise ValueError("host cannot request participation for their own ride")
    stmt = select(RideParticipant).where(
        RideParticipant.rideId == ride_id,
        RideParticipant.userId == user_id
    )
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        raise ValueError("user has either already requested or joined this ride")

    participation = RideParticipant(
        rideId=ride_id,
        userId=user_id,
        status=ParticipantStatus.PENDING,
        requestedAt=datetime.now(timezone.utc)
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)

    return participation


# -------------------------------
# approve ride(done by the host)
# -------------------------------
def decide_participation(
    db: Session,
    host_id: str,
    ride_id: str,
    participant_user_id: str,
    approve: bool
):
    stmt = select(Ride).where(Ride.rideId == ride_id)
    ride = db.execute(stmt).scalar_one_or_none()
    if not ride:
        raise ValueError("Ride not found")
    if ride.hostId != host_id:
        raise ValueError("Only host can approve or reject participants")
    if ride.status != RideStatus.UPCOMING:
        raise ValueError("Cannot modify participants for this ride")
    if participant_user_id == host_id:
        raise ValueError("Host cannot be a participant")

    stmt = select(RideParticipant).where(
        RideParticipant.rideId == ride_id,
        RideParticipant.userId == participant_user_id
    )
    participant = db.execute(stmt).scalar_one_or_none()

    if not participant:
        raise ValueError("Participant request not found")
    if participant.status != ParticipantStatus.PENDING:
        raise ValueError("Participant already decided")

    if approve:
        stmt = select(func.count()).where(
            RideParticipant.rideId == ride_id,
            RideParticipant.status == ParticipantStatus.APPROVED
        )
        approved_count = db.execute(stmt).scalar_one()
        if approved_count >= ride.maxParticipants:
            raise ValueError("Maximum participants limit reached")

        participant.status = ParticipantStatus.APPROVED
    else:
        participant.status = ParticipantStatus.REJECTED

    participant.decisionAt = datetime.now(timezone.utc)

    db.commit()
    db.refresh(participant)

    return participant



# -------------------------------------------------------------------------
# get all details about the ride including all the participants
# -------------------------------------------------------------------------
def get_ride_details(
    db: Session,
    ride_id: str,
    requester_id: str
):
    # Fetch ride with host and participants
    stmt = (
        select(Ride)
        .where(Ride.rideId == ride_id)
        .options(
            selectinload(Ride.host),
            selectinload(Ride.participants).selectinload(RideParticipant.user),
        )
    )

    ride = db.execute(stmt).scalar_one_or_none()

    if not ride:
        raise ValueError("Ride not found")

    is_host = str(ride.hostId) == str(requester_id)

    approved = []
    pending = []
    rejected = []

    for p in ride.participants:
        user_data = {
            "userId": p.user.userId,
            "username": p.user.username,
            "status": p.status.value,
        }

        if p.status == ParticipantStatus.APPROVED:
            approved.append(user_data)

        elif is_host:
            if p.status == ParticipantStatus.PENDING:
                pending.append(user_data)
            elif p.status == ParticipantStatus.REJECTED:
                rejected.append(user_data)

    return {
        "rideId": ride.rideId,
        "rideName": ride.rideName,
        "rideStartTime": ride.rideStartTime,
        "rideStartPoint": ride.rideStartPoint,
        "rideEndPoint": ride.rideEndPoint,
        "rideDuration": ride.rideDuration,
        "haltDuration": ride.haltDuration,
        "routeLink": ride.routeLink,
        "maxParticipants": ride.maxParticipants,
        "status": ride.status.value,
        "host": {
            "userId": ride.host.userId,
            "username": ride.host.username,
        },
        "participants": {
            "approved": approved,
            "pending": pending if is_host else [],
            "rejected": rejected if is_host else [],
        },
    }



# ------------------------------------------------
# leave ride(for participants)
# ------------------------------------------------
def leave_ride(
    db: Session,
    ride_id: str,
    requester_id: str
):
    ride = db.query(Ride).filter(Ride.rideId == ride_id).first()

    if not ride:
        raise ValueError("Ride not found")

    # Host cannot leave — host must cancel instead
    if ride.hostId == requester_id:
        raise PermissionError("Host cannot leave the ride. Cancel it instead.")

    participation = (
        db.query(RideParticipant)
        .filter(
            RideParticipant.rideId == ride_id,
            RideParticipant.userId == requester_id
        )
        .first()
    )

    if not participation:
        raise ValueError("You are not part of this ride")

    db.delete(participation)
    db.commit()

    return {"message": "Successfully left the ride"}


# ------------------------------------------------
# cancel ride(only for the ride host)
# ------------------------------------------------
def cancel_ride(
    db: Session,
    ride_id: str,
    requester_id: str
):
    ride = db.query(Ride).filter(Ride.rideId == ride_id).first()

    if not ride:
        raise ValueError("Ride not found")

    if ride.hostId != requester_id:
        raise PermissionError("Only host can cancel the ride")

    ride.status = RideStatus.CANCELLED

    # Optional: mark all participants cancelled
    for p in ride.participants:
        p.status = ParticipantStatus.REJECTED

    db.commit()

    return {"message": "Ride cancelled successfully"}
