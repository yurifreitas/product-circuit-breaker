from fastapi import APIRouter, HTTPException
from app.models import Client
from app.schemas import WishlistUpdate, ProductOut, WishlistOut
import httpx
from app.circuit_breaker import circuit_breaker
from app.products_mock import mock_product
import logging
from uuid import UUID
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()
PRODUCT_API = "https://challenge-api.luizalabs.com/api/product/"

async def product_exists(product_id: str) -> bool:
    logger.info(f"[CHECK] Verificando produto: {product_id}")
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await circuit_breaker.call(client.get, f"{PRODUCT_API}{product_id}/")
            if response.status_code == 200:
                return True
    except Exception as e:
        logger.warning(f"[FALHA API EXTERNA] {e}")

    fallback = mock_product(product_id)
    logger.info(f"[MOCK CHECK] {product_id} → {fallback is not None}")
    return fallback is not None

@router.post("/{client_id}/add", response_model=WishlistOut)
async def add_to_wishlist(client_id: str, body: WishlistUpdate):
    try:
        client_uuid = UUID(client_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de cliente inválido")

    client = await Client.get(client_uuid)
    print(f"[DEBUG] Cliente: {client}")

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if body.product_id in client.wishlist:
        raise HTTPException(status_code=400, detail="Produto já está na lista")

    if not await product_exists(body.product_id):
        raise HTTPException(status_code=404, detail=f"Produto inválido: {body.product_id}")

    client.wishlist.append(body.product_id)
    await client.save()
    return await build_detailed_wishlist(client)

@router.post("/{client_id}/remove", response_model=WishlistOut)
async def remove_from_wishlist(client_id: str, body: WishlistUpdate):
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if body.product_id not in client.wishlist:
        raise HTTPException(status_code=404, detail="Produto não está na lista")

    client.wishlist.remove(body.product_id)
    await client.save()
    return await build_detailed_wishlist(client)

@router.get("/{client_id}", response_model=WishlistOut)
async def get_wishlist(client_id: str):
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return await build_detailed_wishlist(client)


async def build_detailed_wishlist(client: Client) -> WishlistOut:
    detailed_wishlist = []

    async with httpx.AsyncClient(verify=False) as http:
        for pid in client.wishlist:
            product_data = None
            try:
                r = await circuit_breaker.call(http.get, f"{PRODUCT_API}{pid}/")
                if r.status_code == 200:
                    product_data = r.json()
            except Exception as e:
                logger.warning(f"[FALHA API PRODUTO] {pid}: {e}")

            if product_data is None:
                product_data = mock_product(pid)
                if product_data:
                    logger.info(f"[FALLBACK MOCK] Produto {pid} retornado do mock.")

            if product_data:
                try:
                    detailed_wishlist.append(ProductOut(
                        id=product_data.get("id"),
                        title=product_data.get("title"),
                        image=product_data.get("image"),
                        price=product_data.get("price"),
                        reviewScore=product_data.get("reviewScore")
                    ))
                except Exception as e:
                    logger.warning(f"[PARSE ERRO] Produto {pid}: {e}")

    return WishlistOut(client_id=str(client.id), wishlist=detailed_wishlist)


