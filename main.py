from fastapi import FastAPI

from db import create_db_and_tables
from routers import participants, trips, users

app = FastAPI()
app.include_router(trips.router)
app.include_router(participants.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
