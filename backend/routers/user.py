from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.dependencies import get_db
from models.user import SignupUser, EditUser
from services.user import create_user, edit_user_info, get_all_users, delete_user
from routers.auth import get_current_active_user, get_current_user_from_token, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

#------------------
# get current user
#------------------

@router.get("/users/me/")
async def read_users_me(
    current_user=Depends(get_current_active_user),
):
    return {
        "username": current_user.username,
        "name": current_user.name,
        "bikeName": current_user.bikeName,
    }

#-------------------
# edit current user
#-------------------
@router.put("/users/me")
def edit_profile(
    user: EditUser,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    current_user = get_current_user_from_token(db, token)

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    updated_user = edit_user_info(
        db=db,
        username=current_user.username,
        name=user.name,
        bikeName=user.bikeName,
    )
    return {
        "name": updated_user.name,
        "bikeName": updated_user.bikeName,
    }

#----------------------
# delete current user
#----------------------

@router.delete("/users/me")
def delete_account(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    success = delete_user(db, current_user.username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "Account deleted successfully"}


#---------------------
# signup new user
#---------------------
@router.post("/signup")
def signup(user: SignupUser, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            username=user.username,
            name=user.name,
            bikeName=user.bikeName,
            password=user.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {
        "userId": str(user.userId),
        "username": user.username,
        "name": user.name,
        "bikeName": user.bikeName,
    }


#---------------------------
# get all user from the DB
#---------------------------
@router.get("/users")
def list_all_users(
    db: Session = Depends(get_db),
):
    users = get_all_users(db)

    return [
        {
            "username": u.username,
            "name": u.name,
            "bikeName": u.bikeName,
        }
        for u in users
    ]



