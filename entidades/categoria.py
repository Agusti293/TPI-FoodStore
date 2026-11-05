from entidades.base import Base
from excepciones import DatoInvalidoError


class Categoria(Base):
    __nombre: str
    __descripcion: str
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('El nombre no puede estar vacio')
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('La descripcion no puede estar vacia')
        self.__descripcion = valor.strip()

    def __str__(self) -> str:
        return f'ID: {self.id} | {self.nombre} | {self.descripcion}'
