from typing import Union

from fastapi import FastAPI

app = FastAPI()


logger: Callable = log_requests(app) 
exception_handler: Callable = handle_exceptions(app)

@app.get("/{path}")
async def get_handler(path: str) -> Dict[str, str]:
    return {"path": path}

@app.post("/{path}")
async def post_handler(path: str) -> Dict[str, str]:
    return {"path": path}