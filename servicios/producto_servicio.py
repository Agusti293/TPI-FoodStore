from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones import (DatoInvalidoError, EntidadNoEncontradaError,
                         OperacionNoPermitidaError, FoodStoreError)
from servicios.categoria_servicio import CategoriaServicio


class ProductoServicio:
    __productos: list[Producto]
    __categorias: CategoriaServicio

    def __init__(self, categorias: CategoriaServicio) -> None:
        self.__productos = []
        self.__categorias = categorias

    def listar(self, solo_disponibles: bool = False) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado and
                (not solo_disponibles or (p.disponible and p.stock > 0))]

    def buscar_por_id(self, identificador: int) -> Producto:
        for producto in self.__productos:
            if producto.id == identificador and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError('Producto no encontrado')

    def crear(self, nombre: str, precio: float, descripcion: str, stock: int,
              imagen: str, disponible: bool, categoria: Categoria) -> Producto:
        if not isinstance(categoria, Categoria):
            raise DatoInvalidoError('La categoria no es valida')
        categoria_registrada = self.__categorias.buscar_por_id(categoria.id)
        if categoria_registrada is not categoria:
            raise OperacionNoPermitidaError('La categoria no pertenece al sistema')
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    def editar(self, identificador: int, nombre: str, precio: float, descripcion: str,
               stock: int, imagen: str, disponible: bool) -> Producto:
        producto = self.buscar_por_id(identificador)
        valores_anteriores: tuple[str, float, str, int, str, bool] = (
            producto.nombre, producto.precio, producto.descripcion,
            producto.stock, producto.imagen, producto.disponible
        )
        try:
            producto.nombre = nombre
            producto.precio = precio
            producto.descripcion = descripcion
            producto.stock = stock
            producto.imagen = imagen
            producto.disponible = disponible
        except (FoodStoreError, ValueError, TypeError):
            (producto.nombre, producto.precio, producto.descripcion,
             producto.stock, producto.imagen, producto.disponible) = valores_anteriores
            raise
        return producto

    def eliminar(self, identificador: int) -> None:
        producto = self.buscar_por_id(identificador)
        producto.eliminado = True
