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


def solicitar_entero(mensaje: str) -> int:
    try:
        valor = int(input(mensaje))
    except ValueError as exc:
        raise ParametroServicioInvalidoError(
            "Debe ingresar un número entero."
        ) from exc
    return valor


def ejecutar_simulaciones() -> None:
    sistema = SistemaGestion()
    try:
        sistema.registrar_cliente(
            Cliente("1001", "Ana Pérez", "ana@example.com")
        )
        sala = ReservaSalas("SALA-1", "Sala de reuniones", 25000, 12)
        equipo = AlquilerEquipos("EQ-1", "Portátil", 30000, "Computador")
        asesoria = AsesoriaEspecializada(
            "ASE-1", "Consultoría Python", 50000, "Python"
        )
        sistema.agregar_servicio(sala)
        sistema.agregar_servicio(equipo)
        sistema.agregar_servicio(asesoria)

        print("Costo válido:", sala.calcular_costo(3))
        print("Costo válido:", equipo.calcular_costo(6, incluir_seguro=True))
        print("Costo válido:", asesoria.calcular_costo(2, "Alta"))
        print(sistema.crear_reserva(
            "R-001", "1001", "SALA-1", datetime(2026, 12, 1, 10, 0)
        ))

        try:
            sala.calcular_costo(0)
        except ParametroServicioInvalidoError as exc:
            print("Operación inválida controlada:", exc)

        try:
            sala.disponible = False
            sala.calcular_costo(2)
        except ServicioNoDisponibleError as exc:
            print("Servicio no disponible controlado:", exc)

        try:
            sistema.crear_reserva(
                "R-001", "1001", "SALA-1",
                datetime(2026, 12, 2, 10, 0)
            )
        except ReservaDuplicadaError as exc:
            print("Reserva duplicada controlada:", exc)

        try:
            Cliente("1002", "Cliente inválido", "correo-sin-formato")
        except ParametroServicioInvalidoError as exc:
            print("Cliente inválido controlado:", exc)
    finally:
        print("Simulación finalizada.")


def menu() -> None:
    sistema = SistemaGestion()
    while True:
        print("\n1. Registrar cliente")
        print("2. Agregar servicio")
        print("3. Crear reserva")
        print("4. Ejecutar simulaciones")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                cliente = Cliente(
                    input("Identificación: ").strip(),
                    input("Nombre: ").strip(),
                    input("Correo: ").strip(),
                )
                sistema.registrar_cliente(cliente)
                print("Cliente registrado.")
            elif opcion == "2":
                tipo = input("Tipo (sala/equipo/asesoria): ").strip().lower()
                codigo = input("Código: ").strip()
                nombre = input("Nombre: ").strip()
                tarifa = float(input("Tarifa base: ").replace(",", "."))
                if tipo == "sala":
                    servicio = ReservaSalas(
                        codigo, nombre, tarifa,
                        solicitar_entero("Capacidad: ")
                    )
                elif tipo == "equipo":
                    servicio = AlquilerEquipos(
                        codigo, nombre, tarifa,
                        input("Tipo de equipo: ").strip()
                    )
                elif tipo == "asesoria":
                    servicio = AsesoriaEspecializada(
                        codigo, nombre, tarifa,
                        input("Área experta: ").strip()
                    )
                else:
                    raise ParametroServicioInvalidoError(
                        "Tipo de servicio no reconocido."
                    )
                sistema.agregar_servicio(servicio)
                print("Servicio agregado.")
            elif opcion == "3":
                reserva = sistema.crear_reserva(
                    input("Código reserva: ").strip(),
                    input("Identificación cliente: ").strip(),
                    input("Código servicio: ").strip(),
                    datetime.now(),
                )
                print(reserva)
            elif opcion == "4":
                ejecutar_simulaciones()
            elif opcion == "5":
                print("Hasta pronto.")
                break
            else:
                print("Opción no válida.")
        except (ParametroServicioInvalidoError,
                ServicioNoDisponibleError,
                ReservaDuplicadaError,
                ValueError, KeyError) as exc:
            print("Error:", exc)


if __name__ == "__main__":
    menu()
