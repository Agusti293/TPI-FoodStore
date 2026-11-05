from consola.menu import Menu
from consola.gestiones import gestionar_categorias, gestionar_productos, gestionar_usuarios, gestionar_pedidos


class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f'\n=== FOOD STORE - ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===')
            print('1. Categorias\n2. Productos\n3. Usuarios\n4. Pedidos\n9. Cerrar sesion\n0. Salir')
            opcion = input('Seleccione: ').strip()
            if opcion == '1':
                gestionar_categorias(self._categorias, self._productos)
            elif opcion == '2':
                gestionar_productos(self._productos, self._categorias)
            elif opcion == '3':
                gestionar_usuarios(self._usuarios, self._usuario)
            elif opcion == '4':
                gestionar_pedidos(self._pedidos, self._usuarios, self._productos)
            elif opcion == '9':
                return True
            elif opcion == '0':
                return False
            else:
                print('Opcion invalida')
