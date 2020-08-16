from fastapi import FastAPI

from src.api.v1 import notes, ping
from src.extensions import database, metadata, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router, prefix='/v1')
app.include_router(notes.router, prefix='/v1')
