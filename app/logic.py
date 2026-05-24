import secrets
import string
from sqlalchemy.orm import Session

from app.models import PasswordHistory


def generate_password(length=16, include_digits=True, include_specials=True):
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_specials:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?/"
    return ''.join(secrets.choice(chars) for _ in range(length))


def save_password_to_db(db: Session, password: str):
    entry = PasswordHistory(password=password)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_last_passwords(db: Session, limit=10):
    return db.query(PasswordHistory).order_by(PasswordHistory.created_at.desc()).limit(limit).all()


def clear_password_history(db: Session):
    db.query(PasswordHistory).delete()
    db.commit()
