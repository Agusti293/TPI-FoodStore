from entidades.pedido import Pedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, EntidadNoEncontradaError, OperacionNoPermitidaError


class PedidoServicio:
    __pedidos: list[Pedido]

    def __init__(self) -> None:
        self.__pedidos: list[Pedido] = []

    def listar(self) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario == usuario]

    def buscar_por_id(self, identificador: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == identificador and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError('Pedido no encontrado')

    def crear(self, usuario: Usuario, forma_pago: FormaPago,
              detalles: list[tuple[Producto, int]]) -> Pedido:
        if not isinstance(usuario, Usuario) or usuario.eliminado:
            raise DatoInvalidoError('El usuario no existe o esta eliminado')
        if not isinstance(forma_pago, FormaPago):
            raise DatoInvalidoError('Forma de pago invalida')
        if not detalles:
            raise DatoInvalidoError('El pedido debe tener al menos un detalle')
        pedido = Pedido(usuario, forma_pago)
        for producto, cantidad in detalles:
            pedido.agregar_detalle(cantidad, producto)
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self.__pedidos.append(pedido)
        return pedido

    def actualizar(self, identificador: int, estado: Estado, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        if not isinstance(estado, Estado) or not isinstance(forma_pago, FormaPago):
            raise DatoInvalidoError('Estado o forma de pago invalido')
        estado_anterior = pedido.estado
        if estado != estado_anterior:
            pedido.estado = estado
            if estado == Estado.CANCELADO:
                self.__devolver_stock(pedido)
        pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, identificador: int) -> None:
        pedido = self.buscar_por_id(identificador)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self.__devolver_stock(pedido)
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True

    def __devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
