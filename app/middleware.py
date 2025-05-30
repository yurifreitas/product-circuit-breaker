import logging
import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

LOG_FILE_PATH = "logs/app.log"
os.makedirs("logs", exist_ok=True)  # Garantir que o diretório de logs exista

def setup_logging(app: FastAPI):
    # Configura log padrão (Stream + File)
    logging.basicConfig(
        level=logging.DEBUG,  # Nível de log: DEBUG (mostra todos os logs)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Formato de log com timestamp
        handlers=[
            logging.StreamHandler(),  # Exibe os logs no console
            logging.FileHandler(LOG_FILE_PATH, mode='a', encoding='utf-8'),  # Escreve no arquivo de logs, no modo 'append'
        ],
    )

    logging.info("Logging foi configurado corretamente!")  # Log de teste simples

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()  # Marca o início da requisição

        # Log de requisição
        logging.info(f"Requisição iniciada: {request.method} {request.url.path}")

        try:
            # Processa a requisição e obtém a resposta
            response = await call_next(request)
        except Exception as exc:
            # Log de erro se a requisição falhar
            logging.exception(f"Erro na requisição: {str(exc)}")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

        duration = time.time() - start_time  # Calcula a duração da requisição
        # Log de finalização da requisição
        logging.info(f"Requisição finalizada: {response.status_code}, Duração: {duration:.4f}s")
        return response