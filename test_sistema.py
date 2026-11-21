import unittest
from datetime import datetime

from Cliente import Cliente
from Reserva import ReservaDuplicadaError
from Servicio import ParametroServicioInvalidoError, ServicioNoDisponibleError
from ServiciosEspecializados import (
    AlquilerEquipos,
    AsesoriaEspecializada,
    ReservaSalas,
)
from SistemaGestion import SistemaGestion


class SistemaGestionTests(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaGestion()
        self.cliente = Cliente("1001", "Ana Pérez", "ana@example.com")
        self.sala = ReservaSalas("SALA-1", "Sala", 25000, 12)
        self.sistema.registrar_cliente(self.cliente)
        self.sistema.agregar_servicio(self.sala)

    def test_servicios_concretos_pueden_instanciarse(self):
        self.assertEqual(ReservaSalas.__abstractmethods__, set())
        self.assertEqual(AlquilerEquipos.__abstractmethods__, set())
        self.assertEqual(AsesoriaEspecializada.__abstractmethods__, set())

    def test_operacion_valida(self):
        reserva = self.sistema.crear_reserva(
            "R-1", "1001", "SALA-1", datetime(2026, 12, 1)
        )
        self.assertEqual(reserva.estado, "Confirmada")
        self.assertEqual(self.sala.calcular_costo(2), 59500)

    def test_operacion_invalida(self):
        with self.assertRaises(ParametroServicioInvalidoError):
            self.sala.calcular_costo(0)

    def test_servicio_no_disponible(self):
        self.sala.disponible = False
        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.calcular_costo(2)

    def test_reserva_duplicada(self):
        fecha = datetime(2026, 12, 1)
        self.sistema.crear_reserva("R-1", "1001", "SALA-1", fecha)
        with self.assertRaises(ReservaDuplicadaError):
            self.sistema.crear_reserva("R-1", "1001", "SALA-1", fecha)


if __name__ == "__main__":
    unittest.main()
