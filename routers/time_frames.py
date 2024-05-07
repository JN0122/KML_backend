from fastapi import APIRouter


router = APIRouter(
    prefix="/time-frames",
    tags=["time-frames"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all():
    return "CZAS"
