# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# import random
# import string
# from fastapi.responses import FileResponse


# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def root():
#     return FileResponse("static/index.html")

# settings = {
#     "default_length": 16,
#     "include_digits": True,
#     "include_specials": True
# }


# class SettingsUpdate(BaseModel):
#     default_length: int | None = None
#     include_digits: bool | None = None
#     include_specials: bool | None = None


# class PasswordRequest(BaseModel):
#     length: int | None = None
#     include_digits: bool | None = None
#     include_specials: bool | None = None


# def generate_password(length=None, include_digits=None, include_specials=None):
#     length = length or settings["default_length"]

#     if include_digits is None:
#         include_digits = settings["include_digits"]
#     if include_specials is None:
#         include_specials = settings["include_specials"]

#     chars = string.ascii_letters
#     if include_digits:
#         chars += string.digits
#     if include_specials:
#         chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

#     return ''.join(random.choice(chars) for _ in range(length))


# @app.get("/settings")
# async def get_settings():
#     return settings


# @app.put("/settings")
# async def update_settings(data: SettingsUpdate):
#     if data.default_length is not None:
#         settings["default_length"] = data.default_length
#     if data.include_digits is not None:
#         settings["include_digits"] = data.include_digits
#     if data.include_specials is not None:
#         settings["include_specials"] = data.include_specials

#     return {"status": "ok", "settings": settings}


# @app.post("/password")
# async def password(data: PasswordRequest):
#     pwd = generate_password(
#         data.length,
#         data.include_digits,
#         data.include_specials
#     )
#     return {"password": pwd}