FROM python:3.11-slim

WORKDIR /app

# Instala o Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --with dev
RUN mkdir -p /app/logs

COPY . /app

RUN chown -R nobody:nogroup /app/logs && chmod -R 755 /app/logs

CMD ["uvicorn", "app.main:app","--log-config","log_config.yaml", "--host", "0.0.0.0", "--port", "8001"]
