import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.routes import router
from app.config import settings

app = FastAPI()

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