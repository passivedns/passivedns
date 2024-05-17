from datetime import datetime, timedelta, UTC
from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import (
    APIKeyCookie,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import JWTError, jwt
from starlette.requests import Request
from pydantic import BaseModel

from db.database import ObjectNotFound
from models.user import User, UserRole

from utils import config

SECRET_KEY = config.g.JWT_SECRET_KEY
ALGORITHM = config.g.ALGORITHM
SESSION_STORE = set()
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="apiv2/auth/token", auto_error=False)
cookie_scheme = APIKeyCookie(name="passiveDNS_session", auto_error=False)

auth_router = APIRouter()

class LoginCred(BaseModel):
    identity: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    cookie: str = Depends(cookie_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    request.state.username = None
    if not token and not cookie:
        raise credentials_exception

    # When dealing with cookies, check that we haven't logged out the user.
    if cookie and cookie not in SESSION_STORE:
        raise credentials_exception

    token = token or cookie

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = User.get(username)
    if user is None:
        raise credentials_exception
    request.state.username = user.username
    return user

# Check roles
def check_admin_user_role(current_user: User=Depends(get_current_user)):
    """
    Check if the JWT belongs to a User or an Admin
    :return: error view if condition not reached
    """
    current_username = current_user.username
    user = User.get(current_username)
    if user.role != UserRole.USER.value and user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="not enough permission")
    
    return {"msg":"permission granted"}



def check_scheduler_role(current_user: User=Depends(get_current_user)):
    """
    Check if the JWT belongs to a Scheduler
    :return: error view if condition not reached
    """
    current_username = current_user.username
    user = User.get(current_username)
    if user.role != UserRole.SCHEDULER.value:
        raise HTTPException(status_code=403, detail="not enough permission")
    
    return {"msg":"permission granted"}



def check_admin_role(current_user: User=Depends(get_current_user)):
    """
    Check if the JWT belongs to an Admin
    :return: error view if condition not reached
    """
    current_username = current_user.username
    user = User.get(current_username)
    if user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="not enough permission")

    return {"msg":"permission granted"}


#Routes
@auth_router.post("/token")
def login(response: Response, form_data:LoginCred):
    identity = form_data.identity
    password = form_data.password
    
    try:
        if User.exists_from_email(identity):
            # assume identity is email
            user = User.get_from_email(identity)
        else:
            # assume identity is username
            user = User.get(identity)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=f"error logging in : {str(o)}")

    if not user.verify_password(password):
        raise HTTPException(status_code=401, detail="error logging in")

    # creating JWT
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    response.set_cookie(key="passiveDNS_session", value=access_token, httponly=True)
    SESSION_STORE.add(access_token)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.get("/token")
def check_jwt(token: str = Depends(cookie_scheme)):
    if not token or token not in SESSION_STORE:
        raise HTTPException(status_code=400, detail="invalid token")
    
    return {"msg":"token is valid"}

@auth_router.get("/logout")
def logout(response: Response, cookie: str = Depends(cookie_scheme)):
    response.delete_cookie(key="passiveDNS_session")
    SESSION_STORE.remove(cookie)
    return {"msg": "Logged out"}