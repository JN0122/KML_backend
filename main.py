from fastapi import FastAPI

from database import router as db_router
from database.database import engine, Base, get_session
from delivery import router as delivery_router
from forecast import router as forecast_router
from forecastdelivery import router as forecastdelivery_router
from truck.router import router as truck_router
from station.router import router as station_router

Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True, "tryItOutEnabled": True})

app.include_router(delivery_router.router)
app.include_router(forecast_router.router)
app.include_router(forecastdelivery_router.router)
app.include_router(db_router.router)
app.include_router(truck_router)
app.include_router(station_router)

# run on start
db_router.seed_database(get_session())
