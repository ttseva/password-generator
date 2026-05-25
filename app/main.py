from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import socket

from app.config import settings
from app.routes import router
from app.logger import log

app = FastAPI()

@app.middleware("http")
async def add_server_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Served-By"] = socket.gethostname()
    return response

log.info(
    "Application startup configuration",
    database_url=settings.database_url,
    app_version=settings.app_version,
    app_env=settings.app_env
)
current_dir = Path(__file__).parent

app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")
app.include_router(router)


@app.get("/")
def root():
    return FileResponse(current_dir / "templates" / "index.html")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
