from fastapi import FastAPI
import delivery.model
from routers import time_frame_router

from fastapi import FastAPI, Depends, HTTPException
import delivery
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

app.include_router(time_frame_router.router)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
