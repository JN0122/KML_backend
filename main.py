from fastapi import FastAPI
from routers import time_frames

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": True
    }
)


app.include_router(time_frames.router)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
