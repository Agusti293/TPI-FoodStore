from entidades.base import Base
from entidades.producto import Producto
from excepciones import DatoInvalidoError


class DetallePedido(Base):
    __cantidad: int
    __producto: Producto
    __subtotal: float
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.cantidad = cantidad
        self.__producto: Producto = producto
        self.__subtotal: float = cantidad * producto.precio

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise DatoInvalidoError('La cantidad debe ser mayor a cero')
        self.__cantidad = valor

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def sumar_cantidad(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatoInvalidoError('La cantidad debe ser mayor a cero')
        self.__cantidad += cantidad
        self.__subtotal += cantidad * self.__producto.precio

    def __str__(self) -> str:
        return f'{self.producto.nombre} | Cantidad: {self.cantidad} | Subtotal: ${self.subtotal:.2f}'
