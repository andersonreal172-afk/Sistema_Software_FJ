import logging
from datetime import datetime
from pathlib import Path

from Cliente import Cliente
from Reserva import Reserva, ReservaDuplicadaError
from Servicio import ParametroServicioInvalidoError, Servicio


LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOGGER = logging.getLogger("SistemaSoftwareFJ")
LOGGER.setLevel(logging.DEBUG)

if not LOGGER.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler = logging.FileHandler(LOG_DIR / "sistema.log", encoding="utf-8")
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


class SistemaGestion:
    """Gestión en memoria de clientes, servicios y reservas."""

    def __init__(self):
        self.clientes = {}
        self.servicios = {}
        self.reservas = {}

    def registrar_cliente(self, cliente: Cliente) -> None:
        try:
            if cliente.identificacion in self.clientes:
                raise ParametroServicioInvalidoError(
                    "Ya existe un cliente con esta identificación."
                )
            self.clientes[cliente.identificacion] = cliente
            LOGGER.info("Cliente registrado: %s", cliente.identificacion)
        except ParametroServicioInvalidoError as exc:
            LOGGER.warning("Registro de cliente inválido: %s", exc)
            raise
        else:
            LOGGER.debug("Operación de registro completada correctamente.")

    def agregar_servicio(self, servicio: Servicio) -> None:
        try:
            if not isinstance(servicio, Servicio):
                raise ParametroServicioInvalidoError(
                    "El objeto no corresponde a un servicio válido."
                )
            if servicio.codigo in self.servicios:
                raise ParametroServicioInvalidoError(
                    "Ya existe un servicio con este código."
                )
            self.servicios[servicio.codigo] = servicio
        except ParametroServicioInvalidoError as exc:
            LOGGER.error("No fue posible agregar el servicio: %s", exc)
            raise
        else:
            LOGGER.info("Servicio agregado: %s", servicio.codigo)
        finally:
            LOGGER.debug("Intento de agregar servicio finalizado.")

    def crear_reserva(self, codigo: str, identificacion_cliente: str,
                      codigo_servicio: str, fecha: datetime) -> Reserva:
        try:
            if codigo in self.reservas:
                raise ReservaDuplicadaError(
                    f"La reserva '{codigo}' ya existe."
                )
            cliente = self.clientes[identificacion_cliente]
            servicio = self.servicios[codigo_servicio]
            reserva = Reserva(codigo, cliente, servicio, fecha)
            reserva.confirmar()
        except KeyError as exc:
            LOGGER.error(
                "Referencia inexistente al crear la reserva '%s'", codigo
            )
            raise ParametroServicioInvalidoError(
                "El cliente o el servicio indicado no existe."
            ) from exc
        except ReservaDuplicadaError as exc:
            LOGGER.warning("Reserva duplicada: %s", exc)
            raise
        except (TypeError, ParametroServicioInvalidoError) as exc:
            LOGGER.error("Datos inválidos para reserva '%s': %s", codigo, exc)
            raise
        else:
            self.reservas[codigo] = reserva
            LOGGER.info(
                "Reserva creada: %s | Cliente: %s | Servicio: %s",
                codigo, identificacion_cliente, codigo_servicio
            )
            return reserva
