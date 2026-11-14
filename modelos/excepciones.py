
"""
Excepciones personalizadas del sistema Software FJ.

Este módulo centraliza los errores que pueden presentarse
durante la gestión de clientes, servicios y reservas.
"""


# Excepción general del sistema
class SoftwareFJError(Exception):
    """Excepción base para los errores del sistema Software FJ."""
    pass


# Excepciones relacionadas con clientes
class ClienteError(SoftwareFJError):
    """Errores relacionados con el registro y validación de clientes."""
    pass


# Excepciones relacionadas con servicios
class ServicioError(SoftwareFJError):
    """Excepción base para errores de los servicios."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Se genera cuando un servicio no está disponible."""
    pass


class ParametroServicioInvalidoError(ServicioError):
    """Se genera cuando los parámetros de un servicio son incorrectos."""
    pass


# Excepciones relacionadas con reservas
class ReservaError(SoftwareFJError):
    """Excepción base para errores relacionados con reservas."""
    pass


class ReservaNoEncontradaError(ReservaError):
    """Se genera cuando no se encuentra una reserva."""
    pass


class OperacionReservaInvalidaError(ReservaError):
    """Se genera cuando una operación sobre una reserva no está permitida."""
    pass
