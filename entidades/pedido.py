from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, OperacionNoPermitidaError, StockInsuficienteError


class Pedido(Base, Calculable):
    __usuario: Usuario
    __fecha: date
    __estado: Estado
    __total: float
    __forma_pago: FormaPago
    __detalles: list[DetallePedido]
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if not isinstance(usuario, Usuario) or usuario.eliminado:
            raise OperacionNoPermitidaError('No se puede crear un pedido para un usuario inexistente o eliminado')
        if not isinstance(forma_pago, FormaPago):
            raise DatoInvalidoError('Forma de pago invalida')
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__forma_pago: FormaPago = forma_pago
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        if not isinstance(valor, Estado):
            raise DatoInvalidoError('Estado invalido')
        transiciones: dict[Estado, tuple[Estado, ...]] = {
            Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
            Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO),
            Estado.TERMINADO: (),
            Estado.CANCELADO: ()
        }
        if valor != self.__estado and valor not in transiciones[self.__estado]:
            raise OperacionNoPermitidaError('Transicion de estado no permitida')
        self.__estado = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError('Forma de pago invalida')
        self.__forma_pago = valor

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(producto, Producto):
            raise DatoInvalidoError('Producto invalido')
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatoInvalidoError('La cantidad debe ser mayor a cero')
        if producto.eliminado or not producto.disponible:
            raise OperacionNoPermitidaError('El producto no esta disponible')
        detalle = self.buscar_detalle_por_producto(producto)
        cantidad_actual = detalle.cantidad if detalle is not None else 0
        if cantidad_actual + cantidad > producto.stock:
            raise StockInsuficienteError('Stock insuficiente para el producto seleccionado')
        if detalle is None:
            self.__detalles.append(DetallePedido(cantidad, producto))
        else:
            detalle.sumar_cantidad(cantidad)
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is not None:
            self.__detalles.remove(detalle)
            self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def __str__(self) -> str:
        return (f'ID: {self.id} | {self.usuario.nombre} {self.usuario.apellido} | '
                f'{self.estado.name} | {self.forma_pago.name} | Total: ${self.total:.2f} | {self.fecha}')
