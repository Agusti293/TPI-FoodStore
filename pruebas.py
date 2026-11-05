from typing import Callable
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
from entidades.base import Base
from entidades.pedido import Pedido
from entidades.usuario import Usuario
from consola.menu import crear_menu
from consola.menu_cliente import MenuCliente
from main import main
from enums import Rol, Estado, FormaPago
from excepciones import (DatoInvalidoError, DuplicadoError, EntidadNoEncontradaError,
                         OperacionNoPermitidaError, StockInsuficienteError,
                         CredencialesInvalidasError)
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio


def comprobar_error(tipo_error: type[Exception], operacion: Callable[[], object], nombre: str) -> None:
    try:
        operacion()
    except tipo_error:
        print(f'OK - {nombre}')
    else:
        raise AssertionError(f'Fallo la prueba: {nombre}')


def ejecutar_pruebas() -> None:
    print('=== PRUEBAS DEL SISTEMA ===')
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()

    categoria = categorias.crear('Hamburguesas', 'Comidas principales')
    assert categoria.id > 0
    assert categorias.listar() == [categoria]
    categorias.editar(categoria.id, 'Hamburguesas caseras', 'Comidas principales')
    assert categoria.nombre == 'Hamburguesas caseras'
    print('OK - crear, listar y editar categoria')
    comprobar_error(DuplicadoError, lambda: categorias.crear('HAMBURGUESAS CASERAS', 'Otra'),
                    'categoria duplicada sin distinguir mayusculas')
    comprobar_error(DatoInvalidoError, lambda: categorias.crear('', 'Descripcion'),
                    'categoria con nombre vacio')

    categoria_externa = type(categoria)('Pizzas', 'Categoria externa')
    comprobar_error(EntidadNoEncontradaError,
                    lambda: productos.crear('Pizza', 1000, 'Pizza', 2, '', True, categoria_externa),
                    'categoria que no pertenece al servicio')

    producto = productos.crear('Hamburguesa', 2500, 'Hamburguesa completa', 5,
                               'hamburguesa.jpg', True, categoria)
    productos.editar(producto.id, 'Hamburguesa completa', 2600, 'Hamburguesa completa', 5,
                     'hamburguesa.jpg', True)
    assert producto.precio == 2600
    print('OK - crear y editar producto asociado a categoria registrada')
    comprobar_error(DatoInvalidoError,
                    lambda: productos.crear('Producto', -1, 'Descripcion', 2, '', True, categoria),
                    'precio negativo')
    comprobar_error(DatoInvalidoError,
                    lambda: productos.crear('Producto', 100, 'Descripcion', -1, '', True, categoria),
                    'stock negativo')

    producto_anterior = (producto.nombre, producto.precio, producto.descripcion, producto.stock)
    comprobar_error(DatoInvalidoError,
                    lambda: productos.editar(producto.id, 'Nuevo nombre', -10, 'Cambio', 2, '', True),
                    'edicion invalida de producto')
    assert (producto.nombre, producto.precio, producto.descripcion, producto.stock) == producto_anterior
    print('OK - edicion invalida no modifica parcialmente el producto')

    usuario = usuarios.crear('Juan', 'Perez', 'juan@mail.com', '2611234567', '1234', Rol.USUARIO)
    pedido_temporal = Pedido(usuario, FormaPago.EFECTIVO)
    pedido_temporal.agregar_detalle(1, producto)
    producto.precio = 3000
    pedido_temporal.agregar_detalle(1, producto)
    assert pedido_temporal.detalles[0].subtotal == 5600
    pedido_temporal.calcular_total()
    assert pedido_temporal.total == 5600
    pedido_temporal.eliminar_detalle_por_producto(producto)
    assert pedido_temporal.total == 0 and len(pedido_temporal.detalles) == 0
    producto.precio = 2600
    print('OK - subtotal conserva el precio de cada agregado y elimina detalles')
    admin = usuarios.crear('Ana', 'Perez', 'admin@foodstore.com', '2610000000', 'admin123', Rol.ADMIN)
    comprobar_error(DuplicadoError,
                    lambda: usuarios.crear('Otro', 'Usuario', 'JUAN@MAIL.COM', '123', '1234', Rol.USUARIO),
                    'mail duplicado sin distinguir mayusculas')
    comprobar_error(DatoInvalidoError,
                    lambda: usuarios.crear('Otro', 'Usuario', 'mailinvalido', '123', '1234', Rol.USUARIO),
                    'formato de mail invalido')
    assert usuarios.autenticar('JUAN@mail.com', '1234') == usuario
    usuarios.editar(usuario.id, 'Juan Carlos', 'Perez', 'juan@mail.com', '2611234567', '', Rol.USUARIO)
    assert usuario.nombre == 'Juan Carlos'
    print('OK - editar usuario sin exponer la contrasenia')
    comprobar_error(CredencialesInvalidasError, lambda: usuarios.autenticar('juan@mail.com', 'mal'),
                    'credenciales incorrectas')
    comprobar_error(OperacionNoPermitidaError, lambda: usuarios.eliminar(admin.id, admin),
                    'administrador no puede eliminarse a si mismo')
    print('OK - usuario, autenticacion y proteccion de contrasenia')

    pedido = pedidos.crear(usuario, FormaPago.EFECTIVO, [(producto, 2), (producto, 1)])
    assert pedido.total == 7800
    assert producto.stock == 2
    assert len(pedido.detalles) == 1 and pedido.detalles[0].cantidad == 3
    print('OK - crear pedido, acumular detalle repetido, calcular total y descontar stock')
    comprobar_error(StockInsuficienteError,
                    lambda: pedido.agregar_detalle(3, producto),
                    'control de stock insuficiente')
    comprobar_error(DatoInvalidoError,
                    lambda: pedido.agregar_detalle(0, producto),
                    'cantidad cero')
    stock_antes = producto.stock
    comprobar_error(StockInsuficienteError,
                    lambda: pedidos.crear(usuario, FormaPago.TARJETA, [(producto, 100)]),
                    'pedido sin stock no se guarda')
    assert producto.stock == stock_antes
    print('OK - pedido fallido no modifica stock')

    pedidos.actualizar(pedido.id, Estado.CONFIRMADO, FormaPago.TARJETA)
    assert pedido.estado == Estado.CONFIRMADO and pedido.forma_pago == FormaPago.TARJETA
    pedidos.actualizar(pedido.id, Estado.CANCELADO, FormaPago.EFECTIVO)
    assert producto.stock == 5
    print('OK - cancelar pedido devuelve stock')
    comprobar_error(OperacionNoPermitidaError,
                    lambda: pedidos.actualizar(pedido.id, Estado.CONFIRMADO, FormaPago.EFECTIVO),
                    'no permite cambiar estado terminal')

    pedido_2 = pedidos.crear(usuario, FormaPago.TRANSFERENCIA, [(producto, 1)])
    pedidos.actualizar(pedido_2.id, Estado.CONFIRMADO, FormaPago.TRANSFERENCIA)
    pedidos.actualizar(pedido_2.id, Estado.TERMINADO, FormaPago.TRANSFERENCIA)
    pedidos.eliminar(pedido_2.id)
    assert producto.stock == 4 and pedido_2.eliminado
    assert all(detalle.eliminado for detalle in pedido_2.detalles)
    assert pedido_2.estado == Estado.TERMINADO
    print('OK - eliminar pedido terminado conserva el stock')

    pedido_3 = pedidos.crear(usuario, FormaPago.EFECTIVO, [(producto, 1)])
    pedidos.eliminar(pedido_3.id)
    assert producto.stock == 4 and pedido_3.eliminado
    print('OK - eliminar pedido pendiente devuelve el stock')

    comprobar_error(OperacionNoPermitidaError,
                    lambda: categorias.eliminar(categoria.id, productos.listar()),
                    'no elimina categoria con productos activos')
    productos.eliminar(producto.id)
    categorias.eliminar(categoria.id, productos.listar())
    assert categoria.eliminado
    print('OK - baja logica de producto y categoria')

    menu_cliente = crear_menu(usuario, categorias, productos, usuarios, pedidos)
    assert isinstance(menu_cliente, MenuCliente)
    salida_menu = StringIO()
    with patch('builtins.input', side_effect=['0']), redirect_stdout(salida_menu):
        menu_cliente.mostrar()
    assert 'Ver categorias' in salida_menu.getvalue()
    assert 'Crear' not in salida_menu.getvalue() and 'Eliminar' not in salida_menu.getvalue()
    print('OK - menu cliente solo ofrece consultas')

    salida_login = StringIO()
    with patch('builtins.input', side_effect=['incorrecto', 'incorrecta'] * 3), redirect_stdout(salida_login):
        main()
    assert 'Se agotaron los 3 intentos' in salida_login.getvalue()
    print('OK - inicio de sesion finaliza luego de tres intentos fallidos')

    usuarios.eliminar(usuario.id, admin)
    assert usuario.eliminado
    comprobar_error(CredencialesInvalidasError,
                    lambda: usuarios.autenticar('juan@mail.com', '1234'),
                    'usuario eliminado no puede iniciar sesion')
    comprobar_error(EntidadNoEncontradaError, lambda: productos.buscar_por_id(producto.id),
                    'busqueda de producto eliminado')

    assert not Base.__abstractmethods__ == frozenset()
    assert Pedido.__abstractmethods__ == frozenset()
    print('OK - clases abstractas e interfaz')
    print('=== TODAS LAS PRUEBAS FINALIZARON CORRECTAMENTE ===')


if __name__ == '__main__':
    ejecutar_pruebas()
