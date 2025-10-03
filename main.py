from fastapi import FastAPI

from routers import trips
from database import create_db_and_tables

app = FastAPI()
app.include_router(trips.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


