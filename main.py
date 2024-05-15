from fastapi import FastAPI
from routers import time_frame_router
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException
from delivery import crud, dto, model
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

app.include_router(time_frame_router.router)


@app.get("/deliveries/", response_model=list[dto.Delivery])
def read_deliveries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deliveries = crud.get_deliveries(db, skip=skip, limit=limit)
    return deliveries
