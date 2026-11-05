from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError


class Usuario(Base):
    __nombre: str
    __apellido: str
    __mail: str
    __celular: str
    __contrasenia: str
    __rol: Rol
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str,
                 contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        if not contrasenia.strip():
            raise DatoInvalidoError('La contrasenia no puede estar vacia')
        self.__contrasenia: str = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('El nombre no puede estar vacio')
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('El apellido no puede estar vacio')
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        mail = valor.strip().lower()
        if not mail or '@' not in mail or '.' not in mail:
            raise DatoInvalidoError('El mail no tiene un formato valido')
        self.__mail = mail

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('El celular no puede estar vacio')
        self.__celular = valor.strip()

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError('Rol invalido')
        self.__rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def cambiar_contrasenia(self, contrasenia: str) -> None:
        if not contrasenia.strip():
            raise DatoInvalidoError('La contrasenia no puede estar vacia')
        self.__contrasenia = contrasenia

    def __str__(self) -> str:
        return f'ID: {self.id} | {self.nombre} {self.apellido} | {self.mail} | {self.rol.name}'
