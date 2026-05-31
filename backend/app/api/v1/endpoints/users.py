"""
Endpoints de usuarios
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar si el alias ya existe
    db_user = db.query(UserModel).filter(UserModel.alias == user.alias).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Alias ya registrado")
    
    # Verificar si el email ya existe
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear usuario (simplificado, sin hash de contraseña por ahora)
    new_user = UserModel(
        alias=user.alias,
        email=user.email,
        is_artist=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de usuarios"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar perfil del usuario actual"""
    if user_update.alias:
        current_user.alias = user_update.alias
    if user_update.email:
        current_user.email = user_update.email
    if user_update.is_artist is not None:
        current_user.is_artist = user_update.is_artist
    if user_update.artist_bio:
        current_user.artist_bio = user_update.artist_bio
    if user_update.artist_links:
        current_user.artist_links = user_update.artist_links
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/activate-artist", response_model=User)
async def activate_artist_profile(
    artist_bio: str,
    artist_links: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Activar perfil de artista para el usuario actual"""
    current_user.is_artist = True
    current_user.artist_bio = artist_bio
    if artist_links:
        current_user.artist_links = artist_links
    
    db.commit()
    db.refresh(current_user)
    return current_user
