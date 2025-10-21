from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.crud import user as user_crud
from app.schemas import user as user_schemas

router = APIRouter()

@router.post("/telegram", response_model=user_schemas.Token)
async def authenticate_telegram_user(
    user_data: user_schemas.TelegramAuth,
    db: Session = Depends(get_db)
):
    user = user_crud.get_or_create_telegram_user(db, user_data)
    access_token = create_access_token(data={"sub": user.telegram_id})
    return {"access_token": access_token, "token_type": "bearer"}