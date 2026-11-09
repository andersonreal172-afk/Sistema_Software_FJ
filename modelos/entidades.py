from abc import ABC, abstractmethod


class Entidad(ABC):
    """
    Clase abstracta que representa las entidades generales
    del sistema Software FJ.
    """

    def __init__(self, identificador):
        # Validar que el identificador sea texto
        if not isinstance(identificador, str):
            raise TypeError("El identificador debe ser un texto.")

        identificador = identificador.strip()

        if not identificador:
            raise ValueError("El identificador no puede estar vacío.")

        # Atributo encapsulado
        self.__identificador = identificador

    @property
    def identificador(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self.__identificador

    @abstractmethod
    def obtener_informacion(self):
        """Método que deben implementar las clases derivadas."""
        pass

    @abstractmethod
    def validar_datos(self):
        """Método para validar los datos de cada entidad."""
        pass