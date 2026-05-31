"""
Endpoints para el muro social de sentimientos sonoros
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.social import SocialPost, SocialReaction
from app.schemas.social import SocialPost, SocialPostCreate, SocialReaction, SocialReactionCreate

router = APIRouter()

@router.post("/", response_model=SocialPost)
async def create_social_post(
    post: SocialPostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear una publicación en el muro social"""
    new_post = SocialPost(
        user_id=current_user.id,
        content=post.content,
        track_id=post.track_id,
        mood=post.mood
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[SocialPost])
async def get_social_posts(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Obtener publicaciones del muro social"""
    posts = db.query(SocialPost).order_by(SocialPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.get("/user/{user_id}", response_model=List[SocialPost])
async def get_user_social_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Obtener publicaciones de un usuario específico"""
    posts = db.query(SocialPost).filter(
        SocialPost.user_id == user_id
    ).order_by(SocialPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.post("/{post_id}/react", response_model=SocialReaction)
async def react_to_post(
    post_id: int,
    reaction: SocialReactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reaccionar a una publicación (Klick, heart, o responder con otra pista)"""
    # Verificar que la publicación existe
    post = db.query(SocialPost).filter(SocialPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    new_reaction = SocialReaction(
        post_id=post_id,
        user_id=current_user.id,
        reaction_type=reaction.reaction_type,
        track_response_id=reaction.track_response_id
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction

@router.get("/{post_id}/reactions", response_model=List[SocialReaction])
async def get_post_reactions(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Obtener reacciones de una publicación"""
    reactions = db.query(SocialReaction).filter(
        SocialReaction.post_id == post_id
    ).order_by(SocialReaction.created_at.desc()).all()
    return reactions
