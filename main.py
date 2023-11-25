from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
from starlette.responses import JSONResponse
import logging


def log_requests(app: FastAPI) -> Callable:
    logger = logging.getLogger("requests")

    @app.middleware("http")
    async def log_requests_middleware(
        request: Request, call_next: Callable
    ) -> JSONResponse:
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        return JSONResponse(content=response.body, status_code=200)

    return logger.info


def handle_exceptions(app: FastAPI) -> Callable:
    @app.exception_handler(Exception)
    async def handle_exceptions_middleware(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(content="OK", status_code=200)

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
async def get_handler(path: str) -> dict[str, str]:
    return {"path": path}


@app.post("/{path}")
async def post_handler(path: str) -> dict[str, str]:
    return {"path": path}
