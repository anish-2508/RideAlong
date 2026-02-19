from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SignupUser(BaseModel): 
    username: str
    name: str
    password: str
    bikeName: str

class EditUser(BaseModel): 
    name: Optional[str]= None
    bikeName: Optional[str] = None

class UserInDB(BaseModel): 
    userId: str
    username: str
    name: str
    password: str
    bikeName: str
    createdAt: datetime