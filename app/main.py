from fastapi import FastAPI

from app.api.api import api_router
from app.config import get_config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": get_config().db.ASYNC_DATABASE_URI}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(api_router, prefix=get_config().app.API_PREFIX)
