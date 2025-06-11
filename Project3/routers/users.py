from fastapi import FastAPI, APIRouter, HTTPException, Path, Depends # Depends -> dependancy injection which in programming means that we need to do something before we execute what we are trying to execute
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos, Users
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix = '/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close() 

db_dependancy = Annotated[Session, Depends(get_db)] 
user_dependancy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

""" 
My solution, a bit complicated since I used the payload to do this and believe this has security concers 
@router.get("/current_user")
async def get_user(user: user_dependancy, db: db_dependancy): # type: ignore

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return {"user_name": user.get("username"), 
            "user_first":user.get("user_first"), 
            "user_last":user.get("user_last"), 
            "user_role":user.get("user_role"),
            "user_id": user.get("id")
            }
"""
@router.get("/")
async def get_user(user: user_dependancy, db: db_dependancy): # type: ignore
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Users).filter(Users.id == user.get("id")).first()




@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependancy, 
                          db: db_dependancy,  # type: ignore
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()