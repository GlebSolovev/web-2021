from fastapi import FastAPI
from .routers import end_points

app = FastAPI()

app.include_router(end_points.router)
