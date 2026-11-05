from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones import DuplicadoError, EntidadNoEncontradaError, OperacionNoPermitidaError, FoodStoreError


class CategoriaServicio:
    __categorias: list[Categoria]

    def __init__(self) -> None:
        self.__categorias = []

    def listar(self) -> list[Categoria]:
        return [c for c in self.__categorias if not c.eliminado]

    def buscar_por_id(self, identificador: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == identificador and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError('Categoria no encontrada')

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.lower() == nombre.strip().lower() for c in self.__categorias):
            raise DuplicadoError('Ya existe una categoria con ese nombre')
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def editar(self, identificador: int, nombre: str, descripcion: str) -> Categoria:
        categoria = self.buscar_por_id(identificador)
        if any(c.id != identificador and
               c.nombre.lower() == nombre.strip().lower() for c in self.__categorias):
            raise DuplicadoError('Ya existe una categoria con ese nombre')
        nombre_anterior: str = categoria.nombre
        descripcion_anterior: str = categoria.descripcion
        try:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
        except (FoodStoreError, ValueError, TypeError):
            categoria.nombre = nombre_anterior
            categoria.descripcion = descripcion_anterior
            raise
        return categoria

    def eliminar(self, identificador: int, productos: list[Producto]) -> None:
        categoria = self.buscar_por_id(identificador)
        cantidad = sum(1 for p in productos if p.categoria == categoria and not p.eliminado)
        if cantidad:
            raise OperacionNoPermitidaError(f'La categoria tiene {cantidad} productos activos')
        categoria.eliminado = True
