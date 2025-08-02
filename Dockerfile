FROM python:3.13-slim-bookworm AS base

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv venv
# RUN uv pip install

CMD ["uv", "run", "python", "main.py"]