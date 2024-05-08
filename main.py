from fastapi import FastAPI
from routers import time_frame_router

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

app.include_router(time_frame_router.router)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
