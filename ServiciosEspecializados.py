from Servicio import (
    ParametroServicioInvalidoError,
    Servicio,
    ServicioNoDisponibleError,
)


class ReservaSalas(Servicio):
    """Reserva de una sala por horas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 capacidad: int = 1, horas: int = 1, es_vip: bool = False):
        super().__init__(codigo, nombre, tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroServicioInvalidoError(
                "La capacidad debe ser un entero mayor que cero."
            )
        self.capacidad = capacidad
        self.horas = horas
        self.es_vip = es_vip

    def obtener_descripcion(self) -> str:
        return f"Reserva de Sala: {self.nombre} (Capacidad: {self.capacidad} personas)"

    def calcular_costo(self, horas: int = None, descuento: float = 0.0,
                       impuesto: float = 0.19) -> float:
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"La sala '{self.nombre}' no se encuentra disponible."
            )
        cantidad = self.horas if horas is None else horas
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroServicioInvalidoError(
                "Las horas de reserva deben ser mayores a cero."
            )
        if not 0 <= descuento <= 1 or impuesto < 0:
            raise ParametroServicioInvalidoError(
                "Descuento o impuesto fuera de rango."
            )
        subtotal = self.tarifa_base * cantidad
        total = (subtotal - subtotal * descuento) * (1 + impuesto)
        return round(total, 2)


class AlquilerEquipos(Servicio):
    """Alquiler de equipos por cantidad de tiempo."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 tipo_equipo: str = "General", dias: int = 1,
                 seguro_incluido: bool = False):
        super().__init__(codigo, nombre, tarifa_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ParametroServicioInvalidoError(
                "El tipo de equipo no puede estar vacío."
            )
        self.tipo_equipo = tipo_equipo
        self.dias = dias
        self.seguro_incluido = seguro_incluido

    def obtener_descripcion(self) -> str:
        return f"Alquiler de Equipo: {self.nombre} [{self.tipo_equipo}]"

    def calcular_costo(self, cantidad: int = None, por_dia: bool = True,
                       incluir_seguro: bool = None) -> float:
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El equipo '{self.nombre}' no está disponible actualmente."
            )
        cantidad = self.dias if cantidad is None else cantidad
        seguro = self.seguro_incluido if incluir_seguro is None else incluir_seguro
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroServicioInvalidoError(
                "La cantidad de tiempo (días/horas) debe ser mayor a cero."
            )
        costo_base = self.tarifa_base * cantidad
        costo_seguro = 15000 * cantidad if seguro else 0.0
        descuento = 0.10 if por_dia and cantidad >= 5 else 0.0
        return round(costo_base * (1 - descuento) + costo_seguro, 2)


class AsesoriaEspecializada(Servicio):
    """Asesoría técnica o académica por sesiones."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 area_experto: str = "General", sesiones: int = 1,
                 nivel_especializado: bool = False):
        super().__init__(codigo, nombre, tarifa_base)
        if not isinstance(area_experto, str) or not area_experto.strip():
            raise ParametroServicioInvalidoError(
                "El área del experto no puede estar vacía."
            )
        self.area_experto = area_experto
        self.sesiones = sesiones
        self.nivel_especializado = nivel_especializado

    def obtener_descripcion(self) -> str:
        return f"Asesoría Especializada en {self.area_experto} - {self.nombre}"

    def calcular_costo(self, sesiones: int = None,
                       complejidad: str = "Media") -> float:
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"La asesoría '{self.nombre}' no cuenta con asesores disponibles."
            )
        cantidad = self.sesiones if sesiones is None else sesiones
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroServicioInvalidoError(
                "El número de sesiones debe ser mayor a cero."
            )
        if not isinstance(complejidad, str):
            raise ParametroServicioInvalidoError(
                "La complejidad debe ser una cadena de texto."
            )
        multiplicador = 1.0
        if complejidad.lower() == "alta":
            multiplicador = 1.35
        elif complejidad.lower() == "baja":
            multiplicador = 0.85
        if self.nivel_especializado:
            multiplicador *= 1.15
        return round(self.tarifa_base * cantidad * multiplicador, 2)


# Alias de compatibilidad.
Asesorias = AsesoriaEspecializada
