from abc import ABC, abstractmethod
from datetime import datetime


class Base(ABC):
    __id: int
    __eliminado: bool
    __creado_en: datetime
    __contador: int = 0

    def __init__(self) -> None:
        Base.__contador += 1
        self.__id: int = Base.__contador
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError('El estado de eliminacion debe ser booleano')
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    @abstractmethod
    def __str__(self) -> str:
        ...

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return False
        return self.__id == otro.id
