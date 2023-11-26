import logging
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

handler = logging.FileHandler("yes.log.csv", "a", "utf-8")
formatter = logging.Formatter("%(asctime)s,%(thread)d,%(levelname)s,%(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("yes-man")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class PrintGetRequestDetailsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "favicon.ico" in request.url.path:
            return Response(content="favicon")
        logger.debug(f"{request.method=} {request.url.path=}")
        return Response(content="OK")


app = FastAPI()
app.add_middleware(PrintGetRequestDetailsMiddleware)
