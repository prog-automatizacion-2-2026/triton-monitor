# src/app_operator.py
# ROL 5 - Coordinador de Integración y Flujo CLI

import logging
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
    parser = argparse.ArgumentParser(description="TritonMonitor CLI - Telemetría Multicloud")
    parser.add_argument(
        "proveedores",
        nargs="+",
        choices=["AWS", "Azure", "GCP"],
        help="Proveedores cloud a monitorear"
    )
    parser.add_argument(
        "-c", "--cluster-id",
        type=parse_cluster_id,
        required=True,
        help="Identificador del clúster (ej: cluster-us-east-01)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=parse_timeout,
        default=2.5,
        help="Tiempo de espera en segundos (0.1 a 5.0)"
    )
    parser.add_argument(
        "--chaos",
        action="store_true",
        help="Inyectar fallos de red simulados"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["nominal", "debug", "emergency"],
        default="nominal",
        help="Modo operativo del sistema"
    )
    return parser


async def async_main():
    parser = build_cli_parser()
    args = parser.parse_args()

    logger = setup_triton_logging()
    logger.info("Iniciando TritonMonitor", extra={"cluster_id": args.cluster_id})

    try:
        resultados = await scan_all_providers(
            providers=args.proveedores,
            timeout=args.timeout,
            use_chaos=args.chaos
        )
        logger.info("Escaneo completado exitosamente", extra={"resultados": resultados})

    except* ProviderTimeoutError as group:
        for exc in group.exceptions:
            logger.error(f"Timeout detectado: {exc}")
            for note in getattr(exc, "__notes__", []):
                logger.error(f"  -> {note}")

    except* CorruptedPayloadError as group:
        for exc in group.exceptions:
            logger.warning(f"Respuesta HTTP anómala: {exc}")
            for note in getattr(exc, "__notes__", []):
                logger.warning(f"  -> {note}")

    except* NetworkPeeringError as group:
        for exc in group.exceptions:
            logger.critical(f"Pérdida de conectividad severa: {exc}")
            for note in getattr(exc, "__notes__", []):
                logger.critical(f"  -> {note}")

    except* TritonError as group:
        for exc in group.exceptions:
            logger.error(f"Fallo general del monitor: {exc}")

    finally:
        logger.info("Cerrando aplicación.")
        if hasattr(logger, "listener"):
            logger.listener.stop()
        logging.shutdown()


if __name__ == "__main__":
    asyncio.run(async_main())
