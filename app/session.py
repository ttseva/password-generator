import json
import uuid
import redis
from fastapi import Request, Response
from app.config import settings
from app.logger import log


class SessionManager:
    def __init__(self, redis_url: str):
        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            self.use_redis = True
            log.info("Redis connected successfully")
        except Exception as e:
            log.error("Redis connection failed, falling back to in-memory sessions", error=str(e))
            self.use_redis = False
            self._in_memory_sessions = {}

    def get_session_id(self, request: Request, response: Response) -> str:
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            response.set_cookie(
                "session_id",
                session_id,
                httponly=True,
                max_age=3600 * 24,
                samesite="lax"
            )
        return session_id

    def get(self, session_id: str) -> dict:
        if self.use_redis:
            try:
                data = self.client.get(f"session:{session_id}")
                if data:
                    return json.loads(data)
            except Exception as e:
                log.error("Error reading session from Redis", session_id=session_id, error=str(e))
        else:
            return self._in_memory_sessions.get(session_id, {})
        return {}

    def set(self, session_id: str, data: dict):
        if self.use_redis:
            try:
                self.client.setex(f"session:{session_id}", 3600 * 24, json.dumps(data))
            except Exception as e:
                log.error("Error writing session to Redis", session_id=session_id, error=str(e))
        else:
            self._in_memory_sessions[session_id] = data

    def delete(self, session_id: str):
        if self.use_redis:
            try:
                self.client.delete(f"session:{session_id}")
            except Exception as e:
                log.error("Error deleting session from Redis", session_id=session_id, error=str(e))
        else:
            if session_id in self._in_memory_sessions:
                del self._in_memory_sessions[session_id]


session_manager = SessionManager(settings.redis_url)
