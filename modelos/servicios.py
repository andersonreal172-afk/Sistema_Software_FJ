
"""
Módulo de servicios del sistema Software FJ.

Contiene la clase abstracta Servicio y sus tres clases
especializadas: ReservaSalas, AlquilerEquipos y Asesorias.
"""

from abc import ABC, abstractmethod

from modelos.excepciones import (
    ServicioNoDisponibleError,
    ParametroServicioInvalidoError
)


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):
    """
    Clase abstracta que representa los servicios ofrecidos
    por la empresa Software FJ.
    """

    def __init__(self, codigo, nombre, tarifa_base):

        if not isinstance(codigo, str) or not codigo.strip():
            raise ParametroServicioInvalidoError(
                "El código del servicio es obligatorio."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise ParametroServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        if (
            isinstance(tarifa_base, bool)
            or not isinstance(tarifa_base, (int, float))
            or tarifa_base <= 0
        ):
            raise ParametroServicioInvalidoError(
                "La tarifa base debe ser mayor que cero."
            )

        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):

        if not isinstance(estado, bool):
            raise ParametroServicioInvalidoError(
                "La disponibilidad debe ser un valor booleano."
            )

        self._disponible = estado

    def validar_disponibilidad(self):

        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Calcula el costo según el tipo de servicio."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Devuelve la descripción del servicio."""
        pass


# =====================================================
# 1. RESERVA DE SALAS
# =====================================================

class ReservaSalas(Servicio):
    """
    Servicio especializado para el alquiler de salas por horas.
    Las reservas VIP tienen un recargo del 20%.
    """

    def __init__(self, codigo, nombre, tarifa_base, capacidad=20):

        super().__init__(codigo, nombre, tarifa_base)

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise ParametroServicioInvalidoError(
                "La capacidad debe ser mayor que cero."
            )

        self.capacidad = capacidad

    def obtener_descripcion(self):

        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas."
        )

    def calcular_costo(
        self,
        horas,
        descuento=0.0,
        impuesto=0.0,
        es_vip=False
    ):

        self.validar_disponibilidad()

        if (
            isinstance(horas, bool)
            or not isinstance(horas, int)
            or horas <= 0
        ):
            raise ParametroServicioInvalidoError(
                "Las horas deben ser un entero mayor que cero."
            )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not 0 <= descuento <= 1
        ):
            raise ParametroServicioInvalidoError(
                "El descuento debe estar entre 0 y 1."
            )

        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not 0 <= impuesto <= 1
        ):
            raise ParametroServicioInvalidoError(
                "El impuesto debe estar entre 0 y 1."
            )

        if not isinstance(es_vip, bool):
            raise ParametroServicioInvalidoError(
                "La condición VIP debe ser booleana."
            )

        subtotal = self.tarifa_base * horas

        total = subtotal * (1 - descuento)

        if es_vip:
            total *= 1.20

        total *= (1 + impuesto)

        return round(total, 2)


# =====================================================
# 2. ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipos(Servicio):
    """
    Servicio especializado para el alquiler de equipos
    tecnológicos por días u horas.
    """

    def __init__(
        self,
        codigo,
        nombre,
        tarifa_base,
        tipo_equipo="General"
    ):

        super().__init__(codigo, nombre, tarifa_base)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ParametroServicioInvalidoError(
                "El tipo de equipo es obligatorio."
            )

        self.tipo_equipo = tipo_equipo.strip()

    def obtener_descripcion(self):

        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tipo: {self.tipo_equipo}."
        )

    def calcular_costo(
        self,
        cantidad,
        por_dia=True,
        incluir_seguro=False
    ):

        self.validar_disponibilidad()

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ParametroServicioInvalidoError(
                "La cantidad de días u horas debe ser mayor que cero."
            )

        if not isinstance(por_dia, bool) or not isinstance(incluir_seguro, bool):
            raise ParametroServicioInvalidoError(
                "Las opciones deben ser valores booleanos."
            )

        costo_base = self.tarifa_base * cantidad

        # Descuento del 10% para alquileres de cinco días o más.
        descuento = 0.10 if por_dia and cantidad >= 5 else 0.0

        # Seguro adicional de $15.000 por unidad de tiempo.
        seguro = 15000.0 * cantidad if incluir_seguro else 0.0

        total = (costo_base * (1 - descuento)) + seguro

        return round(total, 2)


# =====================================================
# 3. ASESORÍAS ESPECIALIZADAS
# =====================================================

class Asesorias(Servicio):
    """
    Servicio de consultoría técnica o académica por sesiones.
    El costo depende del nivel de complejidad.
    """

    def __init__(
        self,
        codigo,
        nombre,
        tarifa_base,
        area_experto="General"
    ):

        super().__init__(codigo, nombre, tarifa_base)

        if not isinstance(area_experto, str) or not area_experto.strip():
            raise ParametroServicioInvalidoError(
                "El área de experiencia es obligatoria."
            )

        self.area_experto = area_experto.strip()

    def obtener_descripcion(self):

        return (
            f"Asesoría especializada en {self.area_experto}: "
            f"{self.nombre}."
        )

    def calcular_costo(self, sesiones, complejidad="Media"):

        self.validar_disponibilidad()

        if (
            isinstance(sesiones, bool)
            or not isinstance(sesiones, int)
            or sesiones <= 0
        ):
            raise ParametroServicioInvalidoError(
                "El número de sesiones debe ser mayor que cero."
            )

        if not isinstance(complejidad, str):
            raise ParametroServicioInvalidoError(
                "La complejidad debe ser un texto."
            )

        niveles = {
            "baja": 0.85,
            "media": 1.0,
            "alta": 1.35
        }

        nivel = complejidad.strip().lower()

        if nivel not in niveles:
            raise ParametroServicioInvalidoError(
                "La complejidad debe ser Baja, Media o Alta."
            )

        total = self.tarifa_base * sesiones * niveles[nivel]

        return round(total, 2)
