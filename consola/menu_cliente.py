from consola.menu import Menu
from consola.gestiones import listar_categorias, listar_productos, ver_pedidos_cliente


class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f'\n=== FOOD STORE - CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===')
            print('1. Ver categorias\n2. Ver productos disponibles\n3. Mis pedidos\n4. Mis datos\n9. Cerrar sesion\n0. Salir')
            opcion = input('Seleccione: ').strip()
            if opcion == '1':
                listar_categorias(self._categorias)
            elif opcion == '2':
                listar_productos(self._productos, True)
            elif opcion == '3':
                ver_pedidos_cliente(self._pedidos, self._usuario)
            elif opcion == '4':
                print(f'Nombre: {self._usuario.nombre}\nApellido: {self._usuario.apellido}')
                print(f'Mail: {self._usuario.mail}\nCelular: {self._usuario.celular}\nRol: {self._usuario.rol.name}')
            elif opcion == '9':
                return True
            elif opcion == '0':
                return False
            else:
                print('Opcion invalida')
