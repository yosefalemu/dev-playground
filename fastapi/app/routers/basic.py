from fastapi import APIRouter

from app.dependencies.hello import hello as hello_module

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello world!"}

@router.get("/hello")
async def say_hello(name: str):
    return {"message": hello_module.hello(name=name) + " (from query parameter)"}

@router.get("/hello/{name}")
async def say_hello_path(name:str, test: str | None = None, q: str | None = None):
    if q is not None and test is not None:
        return {"message": hello_module.hello(name=name) + f"from path parameter and query parameter with test: {test} and q: {q}"}
    if q is not None:
        return {"message": hello_module.hello(name=name) + f"from path parameter and query parameter with q: {q}"}
    if test is not None:
        return {"message": hello_module.hello(name=name) + f"from path parameter and query parameter with test: {test}"}
    return {"message": hello_module.hello(name=name) + "(from path parameter)"}
