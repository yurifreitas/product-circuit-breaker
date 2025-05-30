import httpx
import redis
from app.schemas import ProductOut
from app.circuit_breaker import circuit_breaker
import logging
from fastapi import APIRouter, HTTPException
from datetime import timedelta
import json

PRODUCT_API = "https://challenge-api.luizalabs.com/api/product/"
logger = logging.getLogger("product_api")
router = APIRouter()

# Configuração do Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@router.get("/products", response_model=list[ProductOut])
async def list_all_products(MAX_PAGES=10):
    """Lista todos os produtos através da API externa e armazena no cache Redis se necessário."""
    produtos: list[ProductOut] = []
    page = 1

    try:
        while page <= MAX_PAGES:
            cache_key = f"products_page_{page}"  # Chave do Redis para a página atual

            # Verifica se os dados da página já estão no cache Redis
            cached_products = redis_client.get(cache_key)
            if cached_products:
                logger.info(f"[CACHE] Produtos da página {page} obtidos do Redis.")
                produtos.extend(json.loads(cached_products))  # Carrega os produtos do Redis
                page += 1
                continue  # Pular a requisição e ir para a próxima página

            # Se não estiver no cache, faz a requisição à API
            async with httpx.AsyncClient(verify=False) as client:
                r = await circuit_breaker.call(client.get, f"{PRODUCT_API}?page={page}")

                if r.status_code != 200:
                    logger.warning(f"[API] Falha ao buscar página {page} (status={r.status_code})")
                    break

                data = r.json()
                results = data.get("products") or data.get("results") or data

                if not isinstance(results, list) or len(results) == 0:
                    logger.info(f"[API] Nenhum produto na página {page}")
                    break  # Fim da paginação

                # Armazenar os produtos no Redis com expiração de 10 minutos
                redis_client.setex(cache_key, timedelta(minutes=10), json.dumps(results))

                for p in results:
                    try:
                        produtos.append(ProductOut(
                            id=p.get("id"),
                            title=p.get("title"),
                            image=p.get("image"),
                            price=p.get("price"),
                            reviewScore=p.get("reviewScore")
                        ))
                    except Exception as parse_error:
                        logger.warning(f"[API] Erro ao parsear produto: {parse_error}")
                page += 1

        if produtos:
            logger.info(f"[API] Produtos reais carregados: {len(produtos)}")
            return produtos

    except Exception as e:
        logger.warning(f"[FALHA API] Erro geral ao buscar produtos reais: {e}")

    # Fallback → mock
    from app.products_mock import MOCK_PRODUCTS
    logger.info("[MOCK] Retornando produtos do mock.")
    return [
        ProductOut(
            id=p["id"],
            title=p["title"],
            image=p["image"],
            price=p["price"],
            reviewScore=p.get("reviewScore")
        )
        for p in MOCK_PRODUCTS.values()
    ]
