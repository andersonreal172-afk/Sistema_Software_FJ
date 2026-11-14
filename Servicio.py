from abc import ABC, abstractmethod

# Excepciones personalizadas para el manejo robusto de servicios
class ServicioError(Exception):
    """Excepción base para errores relacionados con los servicios."""
    pass

class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando un servicio no está disponible o activo."""
    pass

class ParametroServicioInvalidoError(ServicioError):
    """Se lanza cuando los parámetros de cálculo o duración son inválidos."""
    pass


# Clase abstracta Servicio (Hereda del concepto base del sistema)
class Servicio(ABC):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        self._codigo = codigo
        self._nombre = nombre
        self._tarifa_base = tarifa_base
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
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise ParametroServicioInvalidoError("El estado de disponibilidad debe ser booleano.")
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto para calcular el costo (Polimorfismo / Sobrecarga)."""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto para describir el servicio."""
        pass


# 1. Servicio Especializado: Reserva de Salas
class ReservaSalas(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, nombre, tarifa_base)
        self.capacidad = capacidad

    def obtener_descripcion(self) -> str:
        return f"Reserva de Sala: {self.nombre} (Capacidad: {self.capacidad} personas)"

    # Sobrecarga simulada mediante parámetros opcionales (Tarifa base, con descuento o con impuesto)
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        if horas <= 0:
            raise ParametroServicioInvalidoError("Las horas de reserva deben ser mayores a cero.")
        
        subtotal = self.tarifa_base * horas
        monto_descuento = subtotal * descuento
        monto_impuesto = (subtotal - monto_descuento) * impuesto
        total = (subtotal - monto_descuento) + monto_impuesto
        return round(total, 2)


# 2. Servicio Especializado: Alquiler de Equipos
class AlquilerEquipos(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def obtener_descripcion(self) -> str:
        return f"Alquiler de Equipo: {self.nombre} [{self.tipo_equipo}]"

    # Sobrecarga para alquiler por días o por horas con opción de seguro opcional
    def calcular_costo(self, cantidad: int, por_dia: bool = True, incluir_seguro: bool = False) -> float:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre}' no está disponible actualmente.")
        if cantidad <= 0:
            raise ParametroServicioInvalidoError("La cantidad de tiempo (días/horas) debe ser mayor a cero.")
        
        costo_base = self.tarifa_base * cantidad
        seguro = 15000 * cantidad if incluir_seguro else 0.0
        
        # Descuento corporativo si alquila por más de 5 días
        descuento = 0.10 if por_dia and cantidad >= 5 else 0.0
        
        total = (costo_base * (1 - descuento)) + seguro
        return round(total, 2)


# 3. Servicio Especializado: Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area_experto: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.area_experto = area_experto

    def obtener_descripcion(self) -> str:
        return f"Asesoría Especializada en {self.area_experto} - {self.nombre}"

    # Sobrecarga para calcular costo considerando nivel de complejidad y número de sesiones
    def calcular_costo(self, sesiones: int, complejidad: str = "Media") -> float:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no cuenta con asesores disponibles.")
        if sesiones <= 0:
            raise ParametroServicioInvalidoError("El número de sesiones debe ser mayor a cero.")

        multiplicador = 1.0
        if complejidad.lower() == "alta":
            multiplicador = 1.35
        elif complejidad.lower() == "baja":
            multiplicador = 0.85

        total = self.tarifa_base * sesiones * multiplicador
        return round(total, 2)
