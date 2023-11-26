from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class PrintGetRequestDetailsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"{request.method=} {request.url.path=}")
        return Response(content="OK")


app = FastAPI()
app.add_middleware(PrintGetRequestDetailsMiddleware)


