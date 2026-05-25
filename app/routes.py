from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.logic import generate_password, save_password_to_db, get_last_passwords, clear_password_history
from app.models import PasswordRequest, SettingsUpdate
from app.session import session_manager

router = APIRouter()


@router.get("/settings")
def get_settings(request: Request, response: Response):
    session_id = session_manager.get_session_id(request, response)
    sess = session_manager.get(session_id)

    user_settings = {
        "port": settings.port,
        "host": settings.host,
        "database_url": settings.database_url,
        "app_version": settings.app_version,
        "app_env": settings.app_env,
        "default_length": sess.get("default_length", settings.default_length),
        "include_digits": sess.get("include_digits", settings.include_digits),
        "include_specials": sess.get("include_specials", settings.include_specials),
    }
    return user_settings


@router.put("/settings")
def update_settings(data: SettingsUpdate, request: Request, response: Response):
    session_id = session_manager.get_session_id(request, response)
    sess = session_manager.get(session_id)

    for key in ["default_length", "include_digits", "include_specials"]:
        val = getattr(data, key)
        if val is not None:
            sess[key] = val

    session_manager.set(session_id, sess)

    user_settings = {
        "port": settings.port,
        "host": settings.host,
        "database_url": settings.database_url,
        "app_version": settings.app_version,
        "app_env": settings.app_env,
        "default_length": sess.get("default_length", settings.default_length),
        "include_digits": sess.get("include_digits", settings.include_digits),
        "include_specials": sess.get("include_specials", settings.include_specials),
    }
    return {"status": "ok", "settings": user_settings}


@router.post("/password")
def password(data: PasswordRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    session_id = session_manager.get_session_id(request, response)
    sess = session_manager.get(session_id)

    length = data.length or sess.get("default_length", settings.default_length)
    include_digits = data.include_digits if data.include_digits is not None else sess.get("include_digits", settings.include_digits)
    include_specials = data.include_specials if data.include_specials is not None else sess.get("include_specials", settings.include_specials)

    pwd = generate_password(
        length=length,
        include_digits=include_digits,
        include_specials=include_specials
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
