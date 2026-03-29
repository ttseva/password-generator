from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import PasswordRequest, SettingsUpdate
from app.logic import generate_password, save_password_to_db, get_last_passwords, clear_password_history
from app.config import settings

router = APIRouter()

@router.get("/settings")
def get_settings():
    return settings

@router.put("/settings")
def update_settings(data: SettingsUpdate):
    for key in ["default_length", "include_digits", "include_specials"]:
        val = getattr(data, key)
        if val is not None:
            settings[key] = val
    return {"status": "ok", "settings": settings}

@router.post("/password")
def password(data: PasswordRequest, db: Session = Depends(get_db)):
    pwd = generate_password(
        length=data.length or settings["default_length"],
        include_digits=data.include_digits if data.include_digits is not None else settings["include_digits"],
        include_specials=data.include_specials if data.include_specials is not None else settings["include_specials"]
    )
    save_password_to_db(db, pwd)
    return {"password": pwd}

@router.get("/history")
def history(db: Session = Depends(get_db)):
    return [p.password for p in get_last_passwords(db)]

@router.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    clear_password_history(db)
    return {"status": "ok"}