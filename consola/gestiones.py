from consola.lectura import leer_texto, leer_entero, leer_decimal, leer_opcion_enum, leer_enum_opcional, confirmar
from entidades.producto import Producto
from enums import Rol, Estado, FormaPago
from excepciones import FoodStoreError
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from entidades.usuario import Usuario


def listar_categorias(servicio: CategoriaServicio) -> None:
    categorias = servicio.listar()
    if not categorias:
        print('No hay categorias cargadas')
    for categoria in categorias:
        print(categoria)


def gestionar_categorias(servicio: CategoriaServicio, productos: ProductoServicio) -> None:
    while True:
        print('\n--- CATEGORIAS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver')
        opcion = input('Seleccione: ').strip()
        try:
            if opcion == '1':
                listar_categorias(servicio)
            elif opcion == '2':
                categoria = servicio.crear(leer_texto('Nombre: '), leer_texto('Descripcion: '))
                print(f'Categoria creada con ID {categoria.id}')
            elif opcion == '3':
                listar_categorias(servicio)
                identificador = leer_entero('ID: ', 1)
                actual = servicio.buscar_por_id(identificador)
                nombre = leer_texto(f'Nombre ({actual.nombre}): ', True) or actual.nombre
                descripcion = leer_texto(f'Descripcion ({actual.descripcion}): ', True) or actual.descripcion
                servicio.editar(identificador, nombre, descripcion)
                print('Categoria actualizada')
            elif opcion == '4':
                listar_categorias(servicio)
                identificador = leer_entero('ID: ', 1)
                if confirmar('Confirma la eliminacion? (S/N): '):
                    servicio.eliminar(identificador, productos.listar())
                    print('Categoria eliminada')
            elif opcion == '0':
                return
            else:
                print('Opcion invalida')
        except (FoodStoreError, ValueError) as error:
            print(f'Error: {error}')


def listar_productos(servicio: ProductoServicio, solo_disponibles: bool = False) -> None:
    productos = servicio.listar(solo_disponibles)
    if not productos:
        print('No hay productos cargados')
    for producto in productos:
        print(producto)


def gestionar_productos(servicio: ProductoServicio, categorias: CategoriaServicio) -> None:
    while True:
        print('\n--- PRODUCTOS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver')
        opcion = input('Seleccione: ').strip()
        try:
            if opcion == '1':
                listar_productos(servicio)
            elif opcion == '2':
                listar_categorias(categorias)
                categoria = categorias.buscar_por_id(leer_entero('ID de categoria: ', 1))
                nombre = leer_texto('Nombre: ')
                descripcion = leer_texto('Descripcion: ')
                precio = leer_decimal('Precio: ', 0)
                stock = leer_entero('Stock: ', 0)
                imagen = leer_texto('Imagen: ')
                disponible = confirmar('Disponible? (S/N): ')
                producto = servicio.crear(nombre, precio, descripcion, stock, imagen, disponible, categoria)
                print(f'Producto creado con ID {producto.id}')
            elif opcion == '3':
                listar_productos(servicio)
                identificador = leer_entero('ID: ', 1)
                actual = servicio.buscar_por_id(identificador)
                nombre = leer_texto(f'Nombre ({actual.nombre}): ', True) or actual.nombre
                precio_txt = leer_texto(f'Precio ({actual.precio}): ', True)
                precio = float(precio_txt.replace(',', '.')) if precio_txt else actual.precio
                descripcion = leer_texto(f'Descripcion ({actual.descripcion}): ', True) or actual.descripcion
                stock_txt = leer_texto(f'Stock ({actual.stock}): ', True)
                stock = int(stock_txt) if stock_txt else actual.stock
                imagen = leer_texto(f'Imagen ({actual.imagen}): ', True) or actual.imagen
                disponible_txt = leer_texto(f'Disponible S/N ({"S" if actual.disponible else "N"}): ', True).upper()
                disponible = actual.disponible if not disponible_txt else disponible_txt == 'S'
                if disponible_txt not in ('', 'S', 'N'):
                    raise ValueError('Debe ingresar S o N')
                servicio.editar(identificador, nombre, precio, descripcion, stock, imagen, disponible)
                print('Producto actualizado')
            elif opcion == '4':
                listar_productos(servicio)
                identificador = leer_entero('ID: ', 1)
                if confirmar('Confirma la eliminacion? (S/N): '):
                    servicio.eliminar(identificador)
                    print('Producto eliminado')
            elif opcion == '0':
                return
            else:
                print('Opcion invalida')
        except (FoodStoreError, ValueError) as error:
            print(f'Error: {error}')


def gestionar_usuarios(servicio: UsuarioServicio, sesion: Usuario) -> None:
    while True:
        print('\n--- USUARIOS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver')
        opcion = input('Seleccione: ').strip()
        try:
            if opcion == '1':
                usuarios = servicio.listar()
                if not usuarios:
                    print('No hay usuarios cargados')
                for usuario in usuarios:
                    print(usuario)
            elif opcion == '2':
                nombre = leer_texto('Nombre: ')
                apellido = leer_texto('Apellido: ')
                mail = leer_texto('Mail: ')
                celular = leer_texto('Celular: ')
                contrasenia = leer_texto('Contrasenia: ')
                rol = leer_opcion_enum('Rol: ', Rol)
                usuario = servicio.crear(nombre, apellido, mail, celular, contrasenia, rol)
                print(f'Usuario creado con ID {usuario.id}')
            elif opcion == '3':
                for usuario in servicio.listar():
                    print(usuario)
                identificador = leer_entero('ID: ', 1)
                actual = servicio.buscar_por_id(identificador)
                nombre = leer_texto(f'Nombre ({actual.nombre}): ', True) or actual.nombre
                apellido = leer_texto(f'Apellido ({actual.apellido}): ', True) or actual.apellido
                mail = leer_texto(f'Mail ({actual.mail}): ', True) or actual.mail
                celular = leer_texto(f'Celular ({actual.celular}): ', True) or actual.celular
                contrasenia = leer_texto('Nueva contrasenia (Enter conserva): ', True)
                rol = leer_enum_opcional('Nuevo rol (Enter conserva): ', Rol, actual.rol)
                servicio.editar(identificador, nombre, apellido, mail, celular, contrasenia, rol)
                print('Usuario actualizado')
            elif opcion == '4':
                for usuario in servicio.listar():
                    print(usuario)
                identificador = leer_entero('ID: ', 1)
                if confirmar('Confirma la eliminacion? (S/N): '):
                    servicio.eliminar(identificador, sesion)
                    print('Usuario eliminado')
            elif opcion == '0':
                return
            else:
                print('Opcion invalida')
        except (FoodStoreError, ValueError) as error:
            print(f'Error: {error}')


def gestionar_pedidos(servicio: PedidoServicio, usuarios: UsuarioServicio,
                      productos: ProductoServicio) -> None:
    while True:
        print('\n--- PEDIDOS ---\n1. Listar\n2. Crear\n3. Actualizar estado o forma de pago\n4. Eliminar\n0. Volver')
        opcion = input('Seleccione: ').strip()
        try:
            if opcion == '1':
                pedidos = servicio.listar()
                if not pedidos:
                    print('No hay pedidos cargados')
                for pedido in pedidos:
                    print(pedido)
            elif opcion == '2':
                for usuario in usuarios.listar():
                    print(usuario)
                usuario = usuarios.buscar_por_id(leer_entero('ID de usuario: ', 1))
                forma_pago = leer_opcion_enum('Forma de pago: ', FormaPago)
                detalles: list[tuple[Producto, int]] = []
                while True:
                    listar_productos(productos, True)
                    producto = productos.buscar_por_id(leer_entero('ID de producto: ', 1))
                    cantidad = leer_entero('Cantidad: ', 1)
                    detalles.append((producto, cantidad))
                    if not confirmar('Agregar otro producto? (S/N): '):
                        break
                pedido = servicio.crear(usuario, forma_pago, detalles)
                print(f'Pedido creado con ID {pedido.id} y total ${pedido.total:.2f}')
            elif opcion == '3':
                for pedido in servicio.listar():
                    print(pedido)
                identificador = leer_entero('ID de pedido: ', 1)
                estado = leer_opcion_enum('Estado: ', Estado)
                forma_pago = leer_opcion_enum('Forma de pago: ', FormaPago)
                servicio.actualizar(identificador, estado, forma_pago)
                print('Pedido actualizado')
            elif opcion == '4':
                for pedido in servicio.listar():
                    print(pedido)
                identificador = leer_entero('ID de pedido: ', 1)
                if confirmar('Confirma la eliminacion? (S/N): '):
                    servicio.eliminar(identificador)
                    print('Pedido eliminado')
            elif opcion == '0':
                return
            else:
                print('Opcion invalida')
        except (FoodStoreError, ValueError) as error:
            print(f'Error: {error}')


def ver_pedidos_cliente(servicio: PedidoServicio, usuario: Usuario) -> None:
    pedidos = servicio.listar_por_usuario(usuario)
    if not pedidos:
        print('No hay pedidos cargados')
        return
    for pedido in pedidos:
        print(pedido)
    try:
        identificador = leer_entero('ID de pedido para ver detalles (0 para volver): ', 0)
        if identificador == 0:
            return
        pedido = servicio.buscar_por_id(identificador)
        if pedido.usuario != usuario:
            print('Pedido no encontrado')
            return
        for detalle in pedido.detalles:
            print(detalle)
        print(f'Total: ${pedido.total:.2f}')
    except FoodStoreError as error:
        print(f'Error: {error}')
