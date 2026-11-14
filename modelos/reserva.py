
"""
Módulo de reservas del sistema Software FJ.

Permite crear, confirmar, cancelar y procesar reservas,
relacionando clientes con los servicios disponibles.
"""

from datetime import datetime
from enum import Enum
import logging
import os

from modelos.entidades import Entidad
from modelos.servicios import Servicio

from modelos.excepciones import (
    ReservaError,
    ReservaNoEncontradaError,
    OperacionReservaInvalidaError,
    ServicioNoDisponibleError
)


# =====================================================
# CONFIGURACIÓN DEL REGISTRO DE EVENTOS Y ERRORES
# =====================================================

RUTA_LOGS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "logs"
)

os.makedirs(RUTA_LOGS, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(RUTA_LOGS, "sistema.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


# =====================================================
# ESTADOS DE LAS RESERVAS
# =====================================================

class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:
    """
    Representa una reserva realizada por un cliente
    para utilizar uno de los servicios de Software FJ.
    """

    def __init__(
        self,
        codigo,
        cliente,
        servicio,
        cantidad,
        **parametros_costo
    ):

        # Validar código
        if not isinstance(codigo, str) or not codigo.strip():
            raise ReservaError(
                "El código de la reserva es obligatorio."
            )

        # Validar cliente
        if not isinstance(cliente, Entidad):
            raise ReservaError(
                "La reserva debe estar asociada a un cliente válido."
            )

        # Validar servicio
        if not isinstance(servicio, Servicio):
            raise ReservaError(
                "La reserva debe estar asociada a un servicio válido."
            )

        # Validar duración
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ReservaError(
                "La duración debe ser un entero mayor que cero."
            )

        self._codigo = codigo.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._cantidad = cantidad

        self._parametros_costo = parametros_costo

        self._estado = EstadoReserva.PENDIENTE
        self._fecha_creacion = datetime.now()
        self._costo = None

        logger.info(
            "Reserva %s creada para el cliente %s.",
            self._codigo,
            self._cliente.identificador
        )

    # =================================================
    # PROPIEDADES
    # =================================================

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def estado(self):
        return self._estado

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def costo(self):
        return self._costo

    # =================================================
    # CONFIRMAR RESERVA
    # =================================================

    def confirmar(self):
        """
        Confirma una reserva que se encuentre pendiente.
        """

        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionReservaInvalidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        try:
            self._servicio.validar_disponibilidad()

            self._estado = EstadoReserva.CONFIRMADA

            logger.info(
                "Reserva %s confirmada correctamente.",
                self._codigo
            )

            return True

        except ServicioNoDisponibleError as error:

            logger.exception(
                "No se pudo confirmar la reserva %s.",
                self._codigo
            )

            raise OperacionReservaInvalidaError(
                "No se puede confirmar porque el servicio no está disponible."
            ) from error

    # =================================================
    # CANCELAR RESERVA
    # =================================================

    def cancelar(self):
        """
        Cancela una reserva pendiente o confirmada.
        """

        if self._estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA
        ):
            raise OperacionReservaInvalidaError(
                "La reserva no puede cancelarse en su estado actual."
            )

        self._estado = EstadoReserva.CANCELADA

        logger.info(
            "Reserva %s cancelada correctamente.",
            self._codigo
        )

        return True

    # =================================================
    # PROCESAR RESERVA
    # =================================================

    def procesar(self):
        """
        Calcula el costo y cambia el estado de la reserva
        cuando el procesamiento finaliza correctamente.
        """

        if self._estado != EstadoReserva.CONFIRMADA:
            raise OperacionReservaInvalidaError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        try:

            self._servicio.validar_disponibilidad()

            # Polimorfismo: cada servicio calcula su propio costo.
            costo_calculado = self._servicio.calcular_costo(
                self._cantidad,
                **self._parametros_costo
            )

            if (
                isinstance(costo_calculado, bool)
                or not isinstance(costo_calculado, (int, float))
                or costo_calculado < 0
            ):
                raise ValueError(
                    "El cálculo del costo produjo un valor inválido."
                )

            self._costo = round(costo_calculado, 2)

        except Exception as error:

            logger.exception(
                "Error al procesar la reserva %s.",
                self._codigo
            )

            raise ReservaError(
                f"No fue posible procesar la reserva {self._codigo}."
            ) from error

        else:

            self._estado = EstadoReserva.PROCESADA

            logger.info(
                "Reserva %s procesada. Costo total: %.2f.",
                self._codigo,
                self._costo
            )

            return self._costo

        finally:

            logger.info(
                "Finalizó el intento de procesamiento de la reserva %s.",
                self._codigo
            )

    # =================================================
    # OBTENER INFORMACIÓN DE LA RESERVA
    # =================================================

    def obtener_resumen(self):

        costo = (
            f"${self._costo:,.2f}"
            if self._costo is not None
            else "Pendiente de cálculo"
        )

        return (
            f"Reserva: {self._codigo}\n"
            f"Cliente: {self._cliente.obtener_informacion()}\n"
            f"Servicio: {self._servicio.obtener_descripcion()}\n"
            f"Cantidad: {self._cantidad}\n"
            f"Estado: {self._estado.value}\n"
            f"Costo: {costo}\n"
            f"Fecha: {self._fecha_creacion}"
        )

    def __str__(self):
        return self.obtener_resumen()
