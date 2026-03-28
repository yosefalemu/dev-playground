from typing import Annotated
from fastapi import Header, HTTPException


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="Token query parameter invalid")
