import uuid
from datetime import datetime
from db.database import Base
from typing import Optional


from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
import enum

# -------------------------
# Enums
# -------------------------

class RideStatus(enum.Enum):
    UPCOMING = "UPCOMING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ParticipantStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# -------------------------
# User
# -------------------------

class User(Base):
    __tablename__ = "users"

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    passwordHash: Mapped[str] = mapped_column(String, nullable=False)

    bikeName: Mapped[str] = mapped_column(String(100), nullable=False)

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    rides_hosted = relationship("Ride", back_populates="host")
    ride_participations = relationship("RideParticipant", back_populates="user")
    comments = relationship("Comment", back_populates="user")


# -------------------------
# Ride
# -------------------------

class Ride(Base):
    __tablename__ = "rides"

    rideId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    hostId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.userId", ondelete="CASCADE"),
        nullable=False,
    )

    rideName: Mapped[str] = mapped_column(String(150), nullable=False)

    rideStartTime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    rideStartPoint: Mapped[str] = mapped_column(String(255), nullable=False)
    rideEndPoint: Mapped[str] = mapped_column(String(255), nullable=False)

    rideDuration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    haltDuration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    routeLink: Mapped[str] = mapped_column(String, nullable=False)

    maxParticipants: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[RideStatus] = mapped_column(
        Enum(RideStatus, name="ride_status"),
        nullable=False,
        index=True,
    )

    # Relationships
    host = relationship("User", back_populates="rides_hosted")
    participants = relationship("RideParticipant", back_populates="ride")
    comments = relationship("Comment", back_populates="ride")


# -------------------------
# RideParticipant
# -------------------------

class RideParticipant(Base):
    __tablename__ = "ride_participants"

    rideId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rides.rideId", ondelete="CASCADE"),
        primary_key=True,
    )

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.userId", ondelete="CASCADE"),
        primary_key=True,
    )

    status: Mapped[ParticipantStatus] = mapped_column(
        Enum(ParticipantStatus, name="participant_status"),
        nullable=False,
        index=True,
    )

    requestedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    decisionAt: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    ride = relationship("Ride", back_populates="participants")
    user = relationship("User", back_populates="ride_participations")


# -------------------------
# Comment
# -------------------------

class Comment(Base):
    __tablename__ = "comments"

    commentId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    rideId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rides.rideId", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.userId", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    commentText: Mapped[str] = mapped_column(String, nullable=False)

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    ride = relationship("Ride", back_populates="comments")
    user = relationship("User", back_populates="comments")
