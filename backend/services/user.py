from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import uuid
from datetime import datetime, timezone
from db.models import User
from typing import Optional, List

password_hash = PasswordHash.recommended()


#-------------------
# User operations
#-------------------
def create_user(
    db: Session,
    username: str,
    name: str,
    bikeName: str,
    password: str,
    ) -> User:

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("username already exists")

    hashed_password = password_hash.hash(password)

    new_user = User(
        userId=uuid.uuid4(),
        username=username,
        name=name,
        bikeName=bikeName,
        passwordHash=hashed_password,
        createdAt=datetime.now(timezone.utc),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def edit_user_info(
    db: Session,
    username: str,
    name: Optional[str] = None,
    bikeName: Optional[str] = None,
) -> Optional[User]:

    existing_user = db.query(User).filter(User.username == username).first()

    if not existing_user:
        return None

    if name is not None:
        existing_user.name = name

    if bikeName is not None:
        existing_user.bikeName = bikeName

    db.commit()
    db.refresh(existing_user)

    return existing_user


def delete_user(db: Session, username: str) -> bool:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    db.delete(user)
    db.commit()
    return True

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()



