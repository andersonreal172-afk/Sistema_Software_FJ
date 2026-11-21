import re

from Servicio import ParametroServicioInvalidoError


class Cliente:
    """Representa un cliente del sistema."""

    def __init__(self, identificacion: str, nombre: str, correo: str):
        if not identificacion or not str(identificacion).strip():
            raise ParametroServicioInvalidoError(
                "La identificación no puede estar vacía."
            )
        if not nombre or not str(nombre).strip():
            raise ParametroServicioInvalidoError("El nombre no puede estar vacío.")
        correo = str(correo).strip() if correo is not None else ""
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise ParametroServicioInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )
        self._identificacion = str(identificacion).strip()
        self._nombre = str(nombre).strip()
        self._correo = correo

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    def __str__(self) -> str:
        return f"{self.nombre} ({self.identificacion}) - {self.correo}"
