FROM python:3.11-slim

WORKDIR /app

# Instala o Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

# Instala dependências principais + de desenvolvimento
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --with dev

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
