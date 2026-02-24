# -- Build stage: export Poetry deps --
FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir poetry==1.8.2

WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without dev

# -- Runtime stage --
FROM python:3.12-slim

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup appuser

WORKDIR /app

COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
