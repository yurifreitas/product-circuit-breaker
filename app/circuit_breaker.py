from aiobreaker import CircuitBreaker, CircuitBreakerListener
import logging
from datetime import timedelta

logger = logging.getLogger("circuit_breaker")


class BreakerLogger(CircuitBreakerListener):
    async def state_change(self, cb, old_state, new_state):
        logger.warning(f"[CIRCUIT BREAKER] Estado mudou de {old_state.name} → {new_state.name}")

    async def failure(self, cb, exc):
        logger.warning(f"[CIRCUIT BREAKER] Falha registrada: {exc}")

    async def success(self, cb):
        logger.info("[CIRCUIT BREAKER] Requisição bem-sucedida")


circuit_breaker = CircuitBreaker(
    fail_max=3,
    timeout_duration=timedelta(seconds=15),
    listeners=[BreakerLogger()]
)
