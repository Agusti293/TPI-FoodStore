from abc import ABC, abstractmethod
from entidades.usuario import Usuario
from enums import Rol
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio


class Menu(ABC):
    _usuario: Usuario
    _categorias: CategoriaServicio
    _productos: ProductoServicio
    _usuarios: UsuarioServicio
    _pedidos: PedidoServicio

    def __init__(self, usuario: Usuario, categorias: CategoriaServicio,
                 productos: ProductoServicio, usuarios: UsuarioServicio,
                 pedidos: PedidoServicio) -> None:
        self._usuario: Usuario = usuario
        self._categorias: CategoriaServicio = categorias
        self._productos: ProductoServicio = productos
        self._usuarios: UsuarioServicio = usuarios
        self._pedidos: PedidoServicio = pedidos

    @abstractmethod
    def mostrar(self) -> bool:
        ...


def crear_menu(usuario: Usuario, categorias: CategoriaServicio, productos: ProductoServicio,
               usuarios: UsuarioServicio, pedidos: PedidoServicio) -> Menu:
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, categorias, productos, usuarios, pedidos)
    return MenuCliente(usuario, categorias, productos, usuarios, pedidos)


from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
