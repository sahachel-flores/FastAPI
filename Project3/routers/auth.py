from fastapi import APIRouter,HTTPException, Path, Depends, Request
from pydantic import BaseModel, Field
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWSError # must do pip install "python-jose[cryptography]"
from datetime import timedelta, datetime, timezone
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)


SECRET_KEY = '59f2f19eca257983a97c3c317c7dcf193c9e438789eb6c8525fe0bfc87a23011'
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

"""
This classes contains the users information for the db table
"""
class CreateUserRequest(BaseModel):
    username : str 
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
"""

"""
class Token(BaseModel):
    access_token: str
    token_type: str



# Creating db dependancy
def get_db():
    db = SessionLocal()

    # The yield statement execurtes the prior and the code under the yield. The coder under finally is executed after we obtain a response.
    try:
        # These prints show how code is executed in order
        print("Here1")
        yield db
    
    finally:
        print("Here3")
        db.close() # closing database after we receive a response

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="Project3/templates")

### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints

"""
this function search and return from the database the user we are authentiucating.
"""
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first() # Searching for user in the db

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password): # Checking the input password by hashing it and comparing to db hashed password
        return False
    return user


"""
This function creates and encodes a jwt access token
"""
def create_access_token(username: str, user_id: int, role:str, expire_delta: timedelta):

    encode = {'sub':username, 'id': user_id, 'role': role} # Encoding user and role
    expire = datetime.now(timezone.utc) + expire_delta # Calculating expiration 
    encode.update({'exp':expire}) # updating expiration date
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) # Creating and returning jsw token

"""
Function to try jwt error message 
"""
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try: 
        # decoding payload which contains the information about our user
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # storing user's information
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        #user_first: str = payload.get('first_name')
        #user_last: str = payload.get('last_name')
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

        # returing our user's information
        return {"username": username, 'id':user_id, 'user_role':user_role}
    except JWSError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

"""
This endpoint creates a user and adds it to the database
"""
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,  # type: ignore
                      create_user_request: CreateUserRequest):
    print("creating authenticated users....")
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        # Encrypting password
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

    # install passlib and bcrypt=4.0.1, pyhton-multipart

"""
This endpoint is used to create a jwt token
"""
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency): # type: ignore
    user = authenticate_user(form_data.username, form_data.password, db) # Searching for user in the database

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20)) # Creating access token for the user

    return {'access_token': token, 'token_type': 'bearer'}
