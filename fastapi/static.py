from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")
