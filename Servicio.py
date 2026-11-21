from abc import ABC, abstractmethod


class ServicioError(Exception):
    """Excepción base para errores relacionados con los servicios."""


class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando un servicio no está disponible."""


class ParametroServicioInvalidoError(ServicioError):
    """Se lanza cuando un parámetro no cumple las reglas del sistema."""


class Servicio(ABC):
    """Representa la abstracción común de todos los servicios."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        if not codigo or not str(codigo).strip():
            raise ParametroServicioInvalidoError("El código no puede estar vacío.")
        if not nombre or not str(nombre).strip():
            raise ParametroServicioInvalidoError("El nombre no puede estar vacío.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base < 0:
            raise ParametroServicioInvalidoError(
                "La tarifa base debe ser un número mayor o igual a cero."
            )
        self._codigo = str(codigo).strip()
        self._nombre = str(nombre).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise ParametroServicioInvalidoError(
                "El estado de disponibilidad debe ser booleano."
            )
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el costo según los datos específicos del servicio."""

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Devuelve una descripción legible del servicio."""
