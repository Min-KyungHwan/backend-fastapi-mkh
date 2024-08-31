from fastapi import FastAPI, Depends, Security
from .web import user

app = FastAPI()

app.include_router(user.router)
