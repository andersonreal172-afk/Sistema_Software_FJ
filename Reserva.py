from datetime import datetime

from Cliente import Cliente
from Servicio import ParametroServicioInvalidoError, Servicio


class ReservaError(Exception):
    """Excepción base de reservas."""


class ReservaDuplicadaError(ReservaError):
    """Se lanza cuando se intenta crear una reserva duplicada."""


class Reserva:
    """Vincula un cliente con un servicio y una fecha."""

    def __init__(self, codigo: str, cliente: Cliente,
                 servicio: Servicio, fecha: datetime):
        if not isinstance(cliente, Cliente):
            raise ParametroServicioInvalidoError(
                "El cliente de la reserva no es válido."
            )
        if not isinstance(servicio, Servicio):
            raise ParametroServicioInvalidoError(
                "El servicio de la reserva no es válido."
            )
        if not isinstance(fecha, datetime):
            raise ParametroServicioInvalidoError(
                "La fecha debe ser un objeto datetime."
            )
        if not codigo or not str(codigo).strip():
            raise ParametroServicioInvalidoError(
                "El código de reserva no puede estar vacío."
            )
        self._codigo = str(codigo).strip()
        self._cliente = cliente
        self._servicio = servicio
        self._fecha = fecha
        self._estado = "Pendiente"

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        self._estado = "Confirmada"

    def cancelar(self) -> None:
        self._estado = "Cancelada"

    def __str__(self) -> str:
        return (
            f"Reserva {self.codigo}: {self.cliente.nombre} - "
            f"{self.servicio.nombre} - {self.fecha:%Y-%m-%d %H:%M} "
            f"[{self.estado}]"
        )
