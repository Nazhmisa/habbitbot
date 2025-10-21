from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine
from app.models import user, habit
from app.api.endpoints import auth, habits

user.Base.metadata.create_all(bind=engine)
habit.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])

@app.get("/")
async def root():
    return {"message": "Habit Tracker API"}