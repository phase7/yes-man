from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
from starlette.responses import JSONResponse
import logging

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_requests(app: FastAPI) -> Callable:
    logger = logging.getLogger("requests")

    @app.middleware("http")
    async def log_requests_middleware(
        request: Request, call_next: Callable
    ) -> Response:
        print(request.url)
        response : Response = await call_next(request)
        return response

    return logger.info


def handle_exceptions(app: FastAPI) -> Callable:
    @app.exception_handler(Exception)
    async def handle_exceptions_middleware(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(content="exception occurred in code", status_code=200)

    return print



logger: Callable = log_requests(app)
exception_handler: Callable = handle_exceptions(app)


@app.get("/{path}")
async def get_handler(path: str) -> dict[str, str]:
    return {"path": path}


@app.post("/{path}")
async def post_handler(path: str) -> dict[str, str]:
    return {"path": path}
