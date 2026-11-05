from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import DatoInvalidoError, PrecioInvalidoError


class Producto(Base):
    __nombre: str
    __precio: float
    __descripcion: str
    __stock: int
    __imagen: str
    __disponible: bool
    __categoria: Categoria
    def __init__(self, nombre: str, precio: float, descripcion: str, stock: int,
                 imagen: str, disponible: bool, categoria: Categoria) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        if not isinstance(categoria, Categoria) or categoria.eliminado:
            raise DatoInvalidoError('La categoria no es valida')
        self.__categoria: Categoria = categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('El nombre no puede estar vacio')
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise DatoInvalidoError('El precio debe ser numerico')
        if valor < 0:
            raise PrecioInvalidoError('El precio no puede ser negativo')
        self.__precio = float(valor)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError('La descripcion no puede estar vacia')
        self.__descripcion = valor.strip()

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError('El stock debe ser un numero entero')
        if valor < 0:
            raise DatoInvalidoError('El stock no puede ser negativo')
        self.__stock = valor

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = valor.strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError('La disponibilidad debe ser S o N')
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    def __str__(self) -> str:
        return (f'ID: {self.id} | {self.nombre} | Precio: ${self.precio:.2f} | '
                f'Stock: {self.stock} | Categoria: {self.categoria.nombre}')
