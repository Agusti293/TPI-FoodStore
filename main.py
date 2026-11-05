from consola.menu import crear_menu
from enums import Rol
from excepciones import CredencialesInvalidasError
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()

    usuarios.crear('Ana', 'Perez', 'admin@foodstore.com', '2610000000', 'admin123', Rol.ADMIN)
    usuarios.crear('Juan', 'Gomez', 'cliente@foodstore.com', '2611111111', 'cliente123', Rol.USUARIO)
    categoria = categorias.crear('Hamburguesas', 'Hamburguesas y combos')
    productos.crear('Hamburguesa clasica', 4500, 'Carne, queso y verduras', 10,
                     'hamburguesa.jpg', True, categoria)
    productos.crear('Hamburguesa doble', 6000, 'Doble carne y queso', 5,
                     'doble.jpg', True, categoria)

    continuar = True
    intentos = 0
    while continuar:
        print('\n=== FOOD STORE - INICIO DE SESION ===')
        mail = input('Mail: ').strip()
        contrasenia = input('Contrasenia: ').strip()
        try:
            sesion = usuarios.autenticar(mail, contrasenia)
            intentos = 0
            print(f'\nBienvenido/a, {sesion.nombre} {sesion.apellido} [{sesion.rol.name}]')
            menu = crear_menu(sesion, categorias, productos, usuarios, pedidos)
            continuar = menu.mostrar()
        except CredencialesInvalidasError:
            intentos += 1
            print('Mail o contrasenia incorrectos')
            if intentos >= 3:
                print('Se agotaron los 3 intentos. El programa finaliza')
                return


if __name__ == '__main__':
    main()
