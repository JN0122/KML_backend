from fastapi import FastAPI

from database import engine, Base
from routers import delivery_router as delivery_router
from routers import forecast_router as forecast_router

Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True, "tryItOutEnabled": True})

app.include_router(delivery_router.router)
app.include_router(forecast_router.router)
