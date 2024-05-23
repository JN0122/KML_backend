from fastapi import FastAPI

from database import router as db_router
from database.database import engine, Base
from delivery import router as delivery_router
from forecast import router as forecast_router

Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True, "tryItOutEnabled": True})

app.include_router(delivery_router.router)
app.include_router(forecast_router.router)
app.include_router(db_router.router)
