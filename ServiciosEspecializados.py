from Servicio import Servicio

class ReservaSalas(Servicio):
    """Servicio especializado para el alquiler de espacios físicos por horas."""

    def __init__(self, codigo: str, descripcion: str, tarifa_base: float, horas: int, es_vip: bool = False):
        super().__init__(codigo, descripcion, tarifa_base)
        if horas <= 0:
            raise ValueError("La cantidad de horas debe ser mayor a cero.")
        self.horas = horas
        self.es_vip = es_vip

    def calcular_costo(self) -> float:
        subtotal = self.tarifa_base * self.horas
        return subtotal * 1.20 if self.es_vip else subtotal


class AlquilerEquipos(Servicio):
    """Servicio especializado para préstamo de hardware o equipos por días."""

    def __init__(self, codigo: str, descripcion: str, tarifa_base: float, dias: int, seguro_incluido: bool = True):
        super().__init__(codigo, descripcion, tarifa_base)
        if dias <= 0:
            raise ValueError("Los días de alquiler deben ser mayores a cero.")
        self.dias = dias
        self.seguro_incluido = seguro_incluido

    def calcular_costo(self) -> float:
        subtotal = self.tarifa_base * self.dias
        return subtotal + 15000.0 if self.seguro_incluido else subtotal


class Asesorias(Servicio):
    """Servicio especializado de consultoría técnica o académica por sesiones."""

    def __init__(self, codigo: str, descripcion: str, tarifa_base: float, sesiones: int, nivel_especializado: bool = False):
        super().__init__(codigo, descripcion, tarifa_base)
        if sesiones <= 0:
            raise ValueError("El número de sesiones debe ser mayor a cero.")
        self.sesiones = sesiones
        self.nivel_especializado = nivel_especializado

    def calcular_costo(self) -> float:
        subtotal = self.tarifa_base * self.sesiones
        return subtotal * 1.50 if self.nivel_especializado else subtotal
