
"""
Programa principal del sistema Software FJ.

Integra clientes, servicios y reservas.
Ejecuta operaciones de prueba y controla los errores
para garantizar la continuidad del programa.
"""

from modelos.cliente import Cliente
from modelos.servicios import (
    ReservaSalas,
    AlquilerEquipos,
    Asesorias
)
from modelos.reserva import Reserva


# =====================================================
# LISTAS INTERNAS DEL SISTEMA
# =====================================================

clientes = []
servicios = []
reservas = []


# =====================================================
# FUNCIÓN PARA EJECUTAR Y CONTROLAR LAS PRUEBAS
# =====================================================

def ejecutar_operacion(numero, descripcion, funcion):
    print("\n" + "=" * 60)
    print(f"OPERACIÓN {numero}: {descripcion}")
    print("=" * 60)

    try:
        resultado = funcion()

    except Exception as error:
        print(f"ERROR CONTROLADO: {type(error).__name__}: {error}")

    else:
        if resultado is not None:
            print(resultado)
        else:
            print("Operación realizada correctamente.")

    finally:
        print(f"Finalizó la operación {numero}.")


# =====================================================
# FUNCIONES DE REGISTRO
# =====================================================

def registrar_cliente(identificador, nombre, apellido, correo, telefono):
    cliente = Cliente(
        identificador,
        nombre,
        apellido,
        correo,
        telefono
    )

    clientes.append(cliente)
    return cliente.obtener_informacion()


def registrar_sala(codigo, nombre, tarifa, capacidad):
    servicio = ReservaSalas(
        codigo,
        nombre,
        tarifa,
        capacidad
    )

    servicios.append(servicio)
    return servicio.obtener_descripcion()


def registrar_equipo(codigo, nombre, tarifa, tipo):
    servicio = AlquilerEquipos(
        codigo,
        nombre,
        tarifa,
        tipo
    )

    servicios.append(servicio)
    return servicio.obtener_descripcion()


def registrar_asesoria(codigo, nombre, tarifa, area):
    servicio = Asesorias(
        codigo,
        nombre,
        tarifa,
        area
    )

    servicios.append(servicio)
    return servicio.obtener_descripcion()


def crear_reserva(codigo, cliente, servicio, cantidad, **parametros):
    reserva = Reserva(
        codigo,
        cliente,
        servicio,
        cantidad,
        **parametros
    )

    reservas.append(reserva)
    return reserva.obtener_resumen()


# =====================================================
# EJECUCIÓN DE LAS OPERACIONES SIMULADAS
# =====================================================

def main():

    print("\n")
    print("*" * 60)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("*" * 60)

    # -------------------------------------------------
    # OPERACIÓN 1: Registrar un cliente válido
    # -------------------------------------------------

    ejecutar_operacion(
        1,
        "Registro de cliente válido",
        lambda: registrar_cliente(
            "C001",
            "Carlos",
            "Ramírez",
            "carlos@gmail.com",
            "3101234567"
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 2: Intentar registrar cliente inválido
    # -------------------------------------------------

    ejecutar_operacion(
        2,
        "Registro de cliente con correo inválido",
        lambda: registrar_cliente(
            "C002",
            "María",
            "López",
            "correo_incorrecto",
            "3111234567"
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 3: Registrar una sala
    # -------------------------------------------------

    ejecutar_operacion(
        3,
        "Creación de servicio de reserva de salas",
        lambda: registrar_sala(
            "S001",
            "Sala de conferencias",
            80000,
            30
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 4: Intentar crear servicio inválido
    # -------------------------------------------------

    ejecutar_operacion(
        4,
        "Creación de servicio con tarifa inválida",
        lambda: registrar_sala(
            "S002",
            "Sala pequeña",
            -50000,
            15
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 5: Registrar alquiler de equipos
    # -------------------------------------------------

    ejecutar_operacion(
        5,
        "Creación de servicio de alquiler de equipos",
        lambda: registrar_equipo(
            "S003",
            "Computador portátil",
            50000,
            "Tecnológico"
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 6: Registrar asesoría especializada
    # -------------------------------------------------

    ejecutar_operacion(
        6,
        "Creación de servicio de asesorías",
        lambda: registrar_asesoria(
            "S004",
            "Asesoría en programación",
            100000,
            "Desarrollo de software"
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 7: Crear una reserva válida
    # -------------------------------------------------

    ejecutar_operacion(
        7,
        "Creación de reserva para una sala",
        lambda: crear_reserva(
            "R001",
            clientes[0],
            servicios[0],
            3,
            descuento=0.10,
            impuesto=0.19,
            es_vip=True
        )
    )

    # -------------------------------------------------
    # OPERACIÓN 8: Confirmar la reserva
    # -------------------------------------------------

    ejecutar_operacion(
        8,
        "Confirmación de reserva",
        lambda: reservas[0].confirmar()
    )

    # -------------------------------------------------
    # OPERACIÓN 9: Procesar la reserva
    # -------------------------------------------------

    ejecutar_operacion(
        9,
        "Procesamiento y cálculo del costo",
        lambda: reservas[0].procesar()
    )

    # -------------------------------------------------
    # OPERACIÓN 10: Crear y cancelar una reserva
    # -------------------------------------------------

    def crear_y_cancelar():
        reserva = Reserva(
            "R002",
            clientes[0],
            servicios[1],
            2,
            por_dia=True,
            incluir_seguro=True
        )

        reservas.append(reserva)
        reserva.cancelar()

        return reserva.obtener_resumen()

    ejecutar_operacion(
        10,
        "Creación y cancelación de una reserva",
        crear_y_cancelar
    )

    # -------------------------------------------------
    # OPERACIÓN 11: Intentar confirmar un servicio
    # que no está disponible
    # -------------------------------------------------

    def confirmar_servicio_no_disponible():

        servicio = servicios[2]
        servicio.disponible = False

        reserva = Reserva(
            "R003",
            clientes[0],
            servicio,
            2,
            complejidad="Alta"
        )

        reservas.append(reserva)

        return reserva.confirmar()

    ejecutar_operacion(
        11,
        "Confirmación de reserva con servicio no disponible",
        confirmar_servicio_no_disponible
    )

    # -------------------------------------------------
    # OPERACIÓN 12: Intentar procesar reserva pendiente
    # -------------------------------------------------

    def procesar_reserva_pendiente():

        reserva = Reserva(
            "R004",
            clientes[0],
            servicios[0],
            2
        )

        reservas.append(reserva)

        return reserva.procesar()

    ejecutar_operacion(
        12,
        "Procesamiento de reserva sin confirmar",
        procesar_reserva_pendiente
    )

    # -------------------------------------------------
    # OPERACIÓN 13: Intentar cancelar reserva procesada
    # -------------------------------------------------

    ejecutar_operacion(
        13,
        "Intento de cancelar una reserva procesada",
        lambda: reservas[0].cancelar()
    )

    # -------------------------------------------------
    # OPERACIÓN 14: Mostrar resumen del sistema
    # -------------------------------------------------

    def mostrar_resumen():

        print("\nRESUMEN GENERAL DEL SISTEMA")
        print("-" * 40)
        print(f"Clientes registrados: {len(clientes)}")
        print(f"Servicios registrados: {len(servicios)}")
        print(f"Reservas registradas: {len(reservas)}")

        print("\nLISTADO DE RESERVAS:")

        for reserva in reservas:
            print(
                f"{reserva.codigo} | "
                f"{reserva.estado.value}"
            )

        return "Resumen generado correctamente."

    ejecutar_operacion(
        14,
        "Consulta del resumen general",
        mostrar_resumen
    )

    print("\n")
    print("*" * 60)
    print(" FIN DE LAS PRUEBAS DEL SISTEMA SOFTWARE FJ")
    print("*" * 60)


# =====================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =====================================================

if __name__ == "__main__":
    main()
