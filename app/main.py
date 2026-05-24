from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.routes import router

app = FastAPI()
print(f"Using database: {settings.database_url}")
print(f"App version: {settings.app_version}")
print(f"Environment: {settings.app_env}")
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
