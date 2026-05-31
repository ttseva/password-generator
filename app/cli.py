import argparse
import getpass
import hashlib
import os
import secrets
import subprocess
import sys
import time

import redis
import uvicorn
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.db import SessionLocal
from app.logger import log
from app.models import AdminUser


def wait_for_database(retries: int = 30, delay: int = 2):
    for attempt in range(1, retries + 1):
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db.close()
            return
        except Exception as error:
            db.close()
            log.warning("Database is not ready yet", attempt=attempt, error=str(error))
            time.sleep(delay)
    raise RuntimeError("Database is not ready")


def wait_for_redis(retries: int = 30, delay: int = 2):
    client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    for attempt in range(1, retries + 1):
        try:
            client.ping()
            return client
        except Exception as error:
            log.warning("Redis is not ready yet", attempt=attempt, error=str(error))
            time.sleep(delay)
    raise RuntimeError("Redis is not ready")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"pbkdf2_sha256$100000${salt}${digest.hex()}"


def run_server(args):
    uvicorn.run(
        "app.main:app",
        host=args.host or settings.host,
        port=args.port or settings.port,
    )


def run_migrations(_args):
    wait_for_database()
    command = [sys.executable, "-m", "alembic", "upgrade", "head"]
    log.info("Applying database migrations", command=" ".join(command))
    subprocess.run(command, check=True)
    log.info("Database migrations applied")


def create_admin(args):
    wait_for_database()
    username = args.username or os.getenv("ADMIN_USERNAME")
    password = args.password or os.getenv("ADMIN_PASSWORD")

    if not username:
        username = input("Admin username: ")
    if not password:
        password = getpass.getpass("Admin password: ")

    db = SessionLocal()
    try:
        admin = AdminUser(username=username, password_hash=hash_password(password))
        db.add(admin)
        db.commit()
        log.info("Admin user created", username=username)
    except IntegrityError:
        db.rollback()
        log.warning("Admin user already exists", username=username)
    finally:
        db.close()


def clear_cache(_args):
    client = wait_for_redis()
    deleted = 0
    for key in client.scan_iter("session:*"):
        client.delete(key)
        deleted += 1
    log.info("Cache cleared", deleted_session_keys=deleted)


def build_parser():
    parser = argparse.ArgumentParser(description="Pass-gen application management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    server_parser = subparsers.add_parser("server", help="run the HTTP service")
    server_parser.add_argument("--host", default=None)
    server_parser.add_argument("--port", type=int, default=None)
    server_parser.set_defaults(func=run_server)

    migrate_parser = subparsers.add_parser("migrate", help="apply database migrations and exit")
    migrate_parser.set_defaults(func=run_migrations)

    admin_parser = subparsers.add_parser("create-admin", help="create an administrative user")
    admin_parser.add_argument("--username", default=None)
    admin_parser.add_argument("--password", default=None)
    admin_parser.set_defaults(func=create_admin)

    cache_parser = subparsers.add_parser("clear-cache", help="clear cached session data")
    cache_parser.set_defaults(func=clear_cache)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
