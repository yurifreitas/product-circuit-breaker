import logging
import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

LOG_FILE_PATH = "logs/app.log"
os.makedirs("logs", exist_ok=True)

def setup_logging(app: FastAPI):

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Exibe os logs no console
            logging.FileHandler(LOG_FILE_PATH, mode='a', encoding='utf-8'),
        ],
    )

    logging.info("Logging foi configurado corretamente!")

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        logging.info(f"Requisição iniciada: {request.method} {request.url.path}")

        try:

            response = await call_next(request)
        except Exception as exc:

            logging.exception(f"Erro na requisição: {str(exc)}")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

        duration = time.time() - start_time
        logging.info(f"Requisição finalizada: {response.status_code}, Duração: {duration:.4f}s")
        return response