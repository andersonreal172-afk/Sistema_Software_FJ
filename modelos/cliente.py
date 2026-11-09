from modelos.entidades import Entidad


class Cliente(Entidad):
    """
    Representa a un cliente de la empresa Software FJ.
    Hereda los atributos y métodos de la clase Entidad.
    """

    def __init__(self, identificador, nombre, apellido, correo, telefono):
        # Inicializar la clase padre
        super().__init__(identificador)

        # Validar los datos personales
        self.__nombre = self._validar_nombre(nombre, "nombre")
        self.__apellido = self._validar_nombre(apellido, "apellido")
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    # Validación de nombres y apellidos
    @staticmethod
    def _validar_nombre(valor, campo):
        if not isinstance(valor, str):
            raise TypeError(f"El {campo} debe ser texto.")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"El {campo} no puede estar vacío.")

        if not all(letra.isalpha() or letra.isspace() for letra in valor):
            raise ValueError(f"El {campo} solo debe contener letras.")

        return valor

    # Validación del correo electrónico
    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto.")

        correo = correo.strip()

        if not correo or "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValueError("El correo electrónico no tiene un formato válido.")

        return correo

    # Validación del teléfono
    @staticmethod
    def _validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise TypeError("El teléfono debe ingresarse como texto.")

        telefono = telefono.strip()

        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos.")

        return telefono

    # Propiedades para consultar los datos
    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Implementación de los métodos abstractos
    def obtener_informacion(self):
        return (
            f"Cliente: {self.nombre} {self.apellido} | "
            f"Identificación: {self.identificador} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

    def validar_datos(self):
        return (
            self._validar_nombre(self.nombre, "nombre")
            and self._validar_nombre(self.apellido, "apellido")
            and self._validar_correo(self.correo)
            and self._validar_telefono(self.telefono)
        )