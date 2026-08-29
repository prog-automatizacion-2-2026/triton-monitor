# src/triton_telemetry/logging_engine.py
# ROL 3 - Ingeniero de Formateo Estructurado JSON
# ROL 4 - Ingeniero de Almacenamiento y Desacoplamiento No Bloqueante

import json
import logging
import logging.config
import logging.handlers
import queue
import os
import gzip
import shutil
from datetime import datetime, timezone
from typing import Any, Dict


# --- ROL 4: Callbacks de compresión para la rotación de archivos ---

def gzip_namer(name: str) -> str:
    """TODO(Rol 4): Devolver el nombre del archivo rotado con extensión .gz"""
    raise NotImplementedError


def gzip_rotator(source: str, dest: str):
    """TODO(Rol 4): Comprimir 'source' a 'dest' en formato gzip y eliminar el original."""
    raise NotImplementedError


# --- ROL 3: Formateador JSON recursivo ---

class AsyncJSONFormatter(logging.Formatter):
    """
    Formateador de logs personalizado que convierte los registros de Python a formato JSON.
    Serializa timestamps en ISO 8601 UTC estricto, expande recursivamente ExceptionGroup,
    e incluye taskName, threadName, y cualquier metadato inyectado vía 'extra'.
    """

    def _serialize_exception(self, exc: BaseException) -> Dict[str, Any]:
        data = {
            "class": exc.__class__.__name__,
            "message": str(exc),
            "notes": getattr(exc, "__notes__", []),
        }

        # Soporte para ExceptionGroups (Python 3.11+, PEP 654)
        if isinstance(exc, ExceptionGroup):
            data["nested_exceptions"] = [
                self._serialize_exception(child)
                for child in exc.exceptions
            ]

        # Soporte para excepciones encadenadas (raise Y from X)
        if exc.__cause__ is not None:
            data["cause"] = self._serialize_exception(exc.__cause__)

        return data

    def format(self, record: logging.LogRecord) -> str:
        # 1. Formatear la fecha y hora a ISO-8601 UTC estricto (terminando en 'Z')
        timestamp = datetime.fromtimestamp(
            record.created,
            tz=timezone.utc
        ).isoformat(
            timespec="milliseconds"
        ).replace("+00:00", "Z")

        # 2. Construir la estructura base del registro de log (Payload)
        payload = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "process": record.process,
            "threadName": record.threadName,
            "taskName": getattr(record, "taskName", None),
        }

        # 3. Si el registro contiene una excepción, la serializamos recursivamente
        if record.exc_info:
            exception = record.exc_info[1]
            payload["exception"] = self._serialize_exception(exception)

        # 4. Filtrar atributos estándar del LogRecord para encontrar metadatos custom
        standard_fields = {
            "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
            "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
            "created", "msecs", "relativeCreated", "thread", "threadName",
            "processName", "process", "message", "taskName",
        }

        # 5. Metadatos personalizados (extra={'campo': 'valor'}) van al mismo nivel
        for key, value in record.__dict__.items():
            if key not in standard_fields and not key.startswith("_"):
                payload[key] = value

        # 6. Convertir todo a una cadena JSON limpia
        return json.dumps(payload, ensure_ascii=False, default=str)

# --- ROL 4: Pipeline no bloqueante (QueueHandler + QueueListener) ---

def setup_triton_logging(log_filename: str = "triton_services.log") -> logging.Logger:
    """
    TODO(Rol 4): Configurar dictConfig con:
    - Handler de consola (stdout) y RotatingFileHandler (2MB, 3 backups) con AsyncJSONFormatter
    - Inyectar gzip_namer y gzip_rotator al RotatingFileHandler
    - Envolver todo en QueueHandler + QueueListener para que el logging
      no bloquee el event loop de asyncio
    - Devolver el logger 'triton_monitor' ya configurado
    """
    raise NotImplementedError
