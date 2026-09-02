# src/triton_telemetry/core.py
# ROL 2 - Ingeniero de Concurrencia y Telemetría Asíncrona

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

# Endpoints de inyección de caos (vía httpbin)
CHAOS_ENDPOINTS = {
    "TIMEOUT_TRIGGER": "https://httpbin.org/delay/3",
    "BAD_GATEWAY_TRIGGER": "https://httpbin.org/status/504",
    "CORRUPTED_TRIGGER": "https://httpbin.org/xml",
}


async def query_provider_telemetry(provider: str, timeout: float, use_chaos: bool = False) -> Dict[str, Any]:
    url = PROVIDER_ENDPOINTS[provider]

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        return {
            "provider": provider,
            "status": "NOMINAL",
            "latency_sec": response.elapsed.total_seconds(),
            "payload_id": data.get("id", -1)
        }


async def scan_all_providers(providers: list[str], timeout: float, use_chaos: bool = False) -> list[Dict[str, Any]]:
    """
    TODO(Rol 2): Orquestar las consultas en paralelo con asyncio.TaskGroup.
    Cada tarea individual debe crearse con tg.create_task(..., name=f"Task-{provider}")
    para que quede trazable en los logs.
    """
    raise NotImplementedError