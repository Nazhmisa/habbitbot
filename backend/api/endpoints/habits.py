from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.crud import habit as habit_crud
from app.schemas import habit as habit_schemas
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=habit_schemas.Habit)
def create_habit(
    habit: habit_schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return habit_crud.create_user_habit(db=db, habit=habit, user_id=current_user.id)

@router.get("/", response_model=List[habit_schemas.Habit])
def read_habits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = habit_crud.get_user_habits(db, user_id=current_user.id, skip=skip, limit=limit)
    return habits

@router.put("/{habit_id}", response_model=habit_schemas.Habit)
def update_habit(
    habit_id: int,
    habit: habit_schemas.HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_habit = habit_crud.get_habit(db, habit_id=habit_id)
    if db_habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return habit_crud.update_habit(db=db, habit_id=habit_id, habit=habit)

@router.delete("/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_habit = habit_crud.get_habit(db, habit_id=habit_id)
    if db_habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    habit_crud.delete_habit(db=db, habit_id=habit_id)
    return {"message": "Habit deleted successfully"}