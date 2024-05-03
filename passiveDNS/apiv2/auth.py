from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi.security import (
    APIKeyCookie,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import JWTError, jwt
from starlette.requests import Request

from db.database import ObjectNotFound
from models.user import User
from views.misc import error_view, valid_view
from views.token import token_view

from utils import config

SECRET_KEY = config.g.JWT_SECRET_KEY
ALGORITHM = config.g.ALGORITHM
SESSION_STORE = set()
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="apiv2/auth/token", auto_error=False)
cookie_scheme = APIKeyCookie(name="passiveDNS_session", auto_error=False)

auth_router = APIRouter()


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
    cookie: str = Security(cookie_scheme),
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

    user = User.find(username=username)
    if user is None:
        raise credentials_exception
    request.state.username = user.username
    return user
    
@auth_router.post("/token")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        identity = form_data.username
        password = form_data.password

        if User.exists_from_email(identity):
            # assume identity is email
            user = User.get_from_email(identity)
        else:
            # assume identity is username
            user = User.get(identity)

        if not user.verify_password(password):
            return error_view(401, "error logging in")

        # creating JWT
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        response.set_cookie(key="passiveDNS_session", value=access_token, httponly=True)
        SESSION_STORE.add(access_token)

        return token_view(access_token)

    except ObjectNotFound:
        return error_view(404, "error logging in")


@auth_router.get("/token")
def check_jwt():
    try:
        user = get_current_user
        return valid_view("token is valid")
    except Exception:
        return error_view(400, "invalid token")

