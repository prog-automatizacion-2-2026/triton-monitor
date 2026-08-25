# src/triton_telemetry/core.py
# ROL 2 - Ingeniero de Concurrencia y TelemetrÃ­a AsÃ­ncrona

import asyncio
import logging
import httpx
from typing import Any, Dict
from .exceptions import ProviderTimeoutError, CorruptedPayloadError, NetworkPeeringError

logger = logging.getLogger("triton_monitor")

# Endpoints reales de prueba (nominal)
PROVIDER_ENDPOINTS = {
    "AWS": "https://jsonplaceholder.typicode.com/posts/1",
    "Azure": "https://jsonplaceholder.typicode.com/posts/2",
    "GCP": "https://jsonplaceholder.typicode.com/posts/3",
}

# Endpoints de inyecciÃ³n de caos (vÃ­a httpbin)
CHAOS_ENDPOINTS = {
    "TIMEOUT_TRIGGER": "https://httpbin.org/delay/3",
    "BAD_GATEWAY_TRIGGER": "https://httpbin.org/status/504",
    "CORRUPTED_TRIGGER": "https://httpbin.org/xml",
}


async def query_provider_telemetry(provider: str, timeout: float, use_chaos: bool = False) -> Dict[str, Any]:
    """
    TODO(Rol 2): Consultar el endpoint correspondiente con httpx.AsyncClient.
    - Capturar httpx.TimeoutException -> relanzar como ProviderTimeoutError
      (usar .add_note() para agregar contexto forense)
    - Capturar httpx.HTTPStatusError (via response.raise_for_status())
      -> relanzar como NetworkPeeringError o CorruptedPayloadError segÃºn corresponda
    - Devolver un dict con: provider, status, latency_sec, payload_id
    """
    raise NotImplementedError


async def scan_all_providers(providers: list[str], timeout: float, use_chaos: bool = False) -> list[Dict[str, Any]]:
    """
    TODO(Rol 2): Orquestar las consultas en paralelo con asyncio.TaskGroup.
    Cada tarea individual debe crearse con tg.create_task(..., name=f"Task-{provider}")
    para que quede trazable en los logs.
    """
    raise NotImplementedError
