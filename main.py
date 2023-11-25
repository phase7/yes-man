from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable, Dict, Any
from starlette.responses import Response as StarletteResponse
import logging

def log_requests(app: FastAPI) -> Callable[[Request, Callable], StarletteResponse]:
    logger = logging.getLogger("requests")

    @app.middleware("http") 
    async def log_requests_middleware(request: Request, call_next: Callable) -> StarletteResponse:
        logger.info(f"{request.method} {request.url}")
        response: StarletteResponse = await call_next(request)
        return response

    return logger.info


def handle_exceptions(app: FastAPI) -> Callable[[Request, Exception], str]:
    @app.exception_handler(Exception)
    async def handle_exceptions_middleware(request: Request, exc: Exception) -> str:
        return "OK"
    
    return print


app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


logger: Callable = log_requests(app) 
exception_handler: Callable = handle_exceptions(app)

@app.get("/{path}")
async def get_handler(path: str) -> Dict[str, str]:
    return {"path": path}

@app.post("/{path}")
async def post_handler(path: str) -> Dict[str, str]:
    return {"path": path}