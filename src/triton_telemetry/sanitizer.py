# src/triton_telemetry/sanitizer.py
# ROL 1 - Ingeniero de Robustez de Entradas y Excepciones

import argparse
import re


def parse_timeout(value: str) -> float:
    """
    TODO(Rol 1): Validar que 'value' sea un float en el rango [0.1, 5.0].
    Si no cumple, lanzar argparse.ArgumentTypeError (NO ValueError directo,
    porque argparse necesita ese tipo especÃ­fico para salir con cÃ³digo 2).
    """
    raise NotImplementedError


def parse_cluster_id(value: str) -> str:
    """
    TODO(Rol 1): Validar con regex que 'value' siga el patrÃ³n
    cluster-<region>-<numero_dos_digitos> (ej: cluster-us-east-01).
    Si no cumple, lanzar argparse.ArgumentTypeError.
    """
    raise NotImplementedError
