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
    if use_chaos:
        if provider == "AWS":
            url = CHAOS_ENDPOINTS["TIMEOUT_TRIGGER"]
        elif provider == "Azure":
            url = CHAOS_ENDPOINTS["BAD_GATEWAY_TRIGGER"]
        else:
            url = CHAOS_ENDPOINTS["CORRUPTED_TRIGGER"]
    else:
        url = PROVIDER_ENDPOINTS[provider]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=timeout)
            response.raise_for_status()

            data = response.json()

            return {
                "provider": provider,
                "status": "NOMINAL",
                "latency_sec": response.elapsed.total_seconds(),
                "payload_id": data.get("id", -1)
            }

        except httpx.TimeoutException as err:
            p_err = ProviderTimeoutError(
                f"Se agotó el tiempo de espera ({timeout}s) al conectar con {provider}."
            )
            p_err.add_note(f"Provider_ID: {provider}")
            p_err.add_note(f"Requested_Timeout_Limit: {timeout}s")
            p_err.add_note(f"Target_Endpoint: {url}")
            raise p_err from err

        except httpx.HTTPStatusError as err:
            n_err = NetworkPeeringError(
                f"Fallo de conexión o denegación de ruteo de {provider}. Estatus HTTP: {err.response.status_code}."
            )
            n_err.add_note(f"Provider_ID: {provider}")
            n_err.add_note(f"HTTP_Status_Code: {err.response.status_code}")
            raise n_err from err


async def scan_all_providers(providers: list[str], timeout: float, use_chaos: bool = False) -> list[Dict[str, Any]]:
    tasks = []
    results = []

    async with asyncio.TaskGroup() as tg:
        for provider in providers:
            task = tg.create_task(
                query_provider_telemetry(provider, timeout, use_chaos),
                name=f"Task-{provider}"
            )
            tasks.append(task)

    for task in tasks:
        results.append(task.result())

    return results