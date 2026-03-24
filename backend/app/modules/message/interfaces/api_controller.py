from fastapi import APIRouter
from app.modules.message.infrastructure.repository import MessageRepository

router = APIRouter(prefix="/api")

repo = MessageRepository()

@router.get("/sentiments")
def get_sentiments():
    return repo.get_sentiments()

@router.get("/themes")
def get_themes():
    return repo.get_themes()

@router.get("/messages")
def get_messages():
    return repo.get_recent()