from fastapi import FastAPI

from database import create_db_and_tables
from routers import trips

app = FastAPI()
app.include_router(trips.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
