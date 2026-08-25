# src/app_operator.py
# ROL 5 - Coordinador de IntegraciÃ³n y Flujo CLI

import argparse
import asyncio
from triton_telemetry import (
    setup_triton_logging,
    scan_all_providers,
    parse_timeout,
    parse_cluster_id,
    ProviderTimeoutError,
    NetworkPeeringError,
    CorruptedPayloadError,
    TritonError,
)


def build_cli_parser() -> argparse.ArgumentParser:
    """
    TODO(Rol 5): Configurar argparse con:
    - 'proveedores' (posicional, nargs='+', choices=['AWS','Azure','GCP'])
    - -c/--cluster-id (type=parse_cluster_id, required=True)
    - -t/--timeout (type=parse_timeout, default=2.5)
    - --chaos (action='store_true')
    - -m/--mode (choices=['nominal','debug','emergency'], default='nominal')
    """
    raise NotImplementedError


async def async_main():
    """
    TODO(Rol 5): 
    - Parsear argumentos y loguear el inicio de la operaciÃ³n
    - try: await scan_all_providers(...)
    - except* ProviderTimeoutError / NetworkPeeringError / CorruptedPayloadError / TritonError:
      reportar cada grupo iterando group.exceptions
    - finally: detener el listener de logging (SIN return/break/continue acÃ¡, PEP 765)
    """
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(async_main())
