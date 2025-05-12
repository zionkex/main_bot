FROM python:3.12-slim
WORKDIR /app/bot

COPY pyproject.toml ./

RUN pip install uv
COPY . ./
RUN uv venv
RUN uv sync
