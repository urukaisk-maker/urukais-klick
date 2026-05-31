"""
Endpoints de autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash
)
from app.core.config import settings
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, User
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el alias ya existe
    db_user = db.query(UserModel).filter(UserModel.alias == user.alias).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El alias ya está registrado"
        )
    
    # Verificar si el email ya existe
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )
    
    # Crear usuario
    hashed_password = get_password_hash(user.password) if user.password else None
    new_user = UserModel(
        alias=user.alias,
        email=user.email,
        hashed_password=hashed_password,
        is_artist=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-anonymous", response_model=Token)
async def login_anonymous(db: Session = Depends(get_db)):
    """Crear sesión anónima temporal"""
    # Generar usuario anónimo temporal
    import uuid
    anonymous_alias = f"anon_{uuid.uuid4().hex[:8]}"
    anonymous_email = f"{anonymous_alias}@temp.urukais"
    
    new_user = UserModel(
        alias=anonymous_alias,
        email=anonymous_email,
        hashed_password=None,
        is_artist=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
