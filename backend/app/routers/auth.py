# backend/app/routers/auth.py

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt
from app.config import settings
from app.db import get_session
from app.models import User, Credential
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(
    req: RegisterRequest,
    session: Session = Depends(get_session)
):
    # Verify that the email is not already registered
    existing = session.exec(
        select(User).where(User.email == req.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    # Create user (optional name, default before '@')
    user_name = req.name or req.email.split("@")[0]
    user = User(email=req.email, name=user_name)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create credential
    cred = Credential(
        user_id=user.id,
        password_hash=get_password_hash(req.password)
    )
    session.add(cred)
    session.commit()

    # Generate tokens
    access_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )
    refresh_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(days=7)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login"
)
def login(
    req: LoginRequest,
    session: Session = Depends(get_session)
):
    # Retrieve user and credential
    user = session.exec(
        select(User).where(User.email == req.email)
    ).first()
    if not user or not user.credential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(req.password, user.credential.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens
    access_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )
    refresh_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(days=7)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id
    )

