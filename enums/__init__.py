from enum import Enum


class Rol(Enum):
    ADMIN = 1
    USUARIO = 2


class Estado(Enum):
    PENDIENTE = 1
    CONFIRMADO = 2
    TERMINADO = 3
    CANCELADO = 4


class FormaPago(Enum):
    TARJETA = 1
    TRANSFERENCIA = 2
    EFECTIVO = 3
