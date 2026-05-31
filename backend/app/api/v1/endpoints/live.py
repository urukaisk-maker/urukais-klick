"""
Endpoints para salas de escucha en directo (LiveKlick)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.live import LiveRoom, LiveChatMessage, LiveReaction
from app.schemas.live import LiveRoom, LiveRoomCreate, LiveChatMessage, LiveChatMessageCreate, LiveReaction, LiveReactionCreate
from datetime import datetime

router = APIRouter()

@router.post("/rooms", response_model=LiveRoom)
async def create_live_room(
    room: LiveRoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva sala de escucha en directo"""
    new_room = LiveRoom(
        host_id=current_user.id,
        title=room.title,
        description=room.description,
        max_listeners=room.max_listeners,
        is_active=True
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/rooms", response_model=List[LiveRoom])
async def get_active_rooms(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Obtener salas activas"""
    rooms = db.query(LiveRoom).filter(
        LiveRoom.is_active == True
    ).order_by(LiveRoom.created_at.desc()).offset(skip).limit(limit).all()
    return rooms

@router.get("/rooms/{room_id}", response_model=LiveRoom)
async def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una sala específica"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room

@router.post("/rooms/{room_id}/end")
async def end_room(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Terminar una sala de escucha"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    if room.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el host puede terminar la sala")
    
    room.is_active = False
    room.ended_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Sala terminada exitosamente"}

@router.post("/rooms/{room_id}/chat", response_model=LiveChatMessage)
async def send_chat_message(
    room_id: int,
    message: LiveChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enviar mensaje al chat de una sala"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    if not room.is_active:
        raise HTTPException(status_code=400, detail="La sala no está activa")
    
    new_message = LiveChatMessage(
        room_id=room_id,
        user_id=current_user.id,
        message=message.message,
        message_type=message.message_type
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/rooms/{room_id}/chat", response_model=List[LiveChatMessage])
async def get_room_chat(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener mensajes del chat de una sala"""
    messages = db.query(LiveChatMessage).filter(
        LiveChatMessage.room_id == room_id
    ).order_by(LiveChatMessage.created_at.desc()).offset(skip).limit(limit).all()
    return messages

@router.post("/rooms/{room_id}/react", response_model=LiveReaction)
async def send_reaction(
    room_id: int,
    reaction: LiveReactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enviar reacción a una sala"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    if not room.is_active:
        raise HTTPException(status_code=400, detail="La sala no está activa")
    
    new_reaction = LiveReaction(
        room_id=room_id,
        user_id=current_user.id,
        reaction_type=reaction.reaction_type
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction

@router.post("/rooms/{room_id}/join")
async def join_room(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Unirse a una sala (incrementar contador de oyentes)"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    if not room.is_active:
        raise HTTPException(status_code=400, detail="La sala no está activa")
    
    if room.current_listeners >= room.max_listeners:
        raise HTTPException(status_code=400, detail="Sala llena")
    
    room.current_listeners += 1
    db.commit()
    
    return {"message": "Te has unido a la sala", "current_listeners": room.current_listeners}

@router.post("/rooms/{room_id}/leave")
async def leave_room(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Salir de una sala (decrementar contador de oyentes)"""
    room = db.query(LiveRoom).filter(LiveRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    if room.current_listeners > 0:
        room.current_listeners -= 1
        db.commit()
    
    return {"message": "Has salido de la sala", "current_listeners": room.current_listeners}
