# src/triton_telemetry/exceptions.py
# ROL 1 - Ingeniero de Robustez de Entradas y Excepciones

# TODO(Rol 1): Crear la excepción base TritonError heredando de Exception
# (NUNCA de BaseException, para no capturar señales de sistema como Ctrl+C)
class TritonError(Exception):
    pass


# TODO(Rol 1): Subclase para timeouts de red
class ProviderTimeoutError(TritonError):
    pass


# TODO(Rol 1): Subclase para respuestas corruptas o estatus HTTP fallidos
class CorruptedPayloadError(TritonError):
    pass


# TODO(Rol 1): Subclase para fallos de DNS o resolución de hosts
class NetworkPeeringError(TritonError):
    pass
