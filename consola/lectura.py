from enum import Enum


def leer_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print('El texto no puede estar vacio')


def leer_entero(mensaje: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f'El valor debe ser como minimo {minimo}')
            else:
                return valor
        except ValueError:
            print('Ingrese un numero entero valido')


def leer_decimal(mensaje: str, minimo: float | None = None) -> float:
    while True:
        try:
            valor = float(input(mensaje).replace(',', '.'))
            if minimo is not None and valor < minimo:
                print(f'El valor debe ser como minimo {minimo}')
            else:
                return valor
        except ValueError:
            print('Ingrese un numero valido')


def leer_opcion_enum(mensaje: str, enumerado: type[Enum]) -> Enum:
    opciones = list(enumerado)
    for indice, opcion in enumerate(opciones, 1):
        print(f'{indice}. {opcion.name}')
    while True:
        valor = leer_entero(mensaje, 1)
        if valor <= len(opciones):
            return opciones[valor - 1]
        print('Opcion fuera de rango')


def confirmar(mensaje: str) -> bool:
    while True:
        valor = input(mensaje).strip().upper()
        if valor in ('S', 'N'):
            return valor == 'S'
        print('Ingrese S o N')


def leer_enum_opcional(mensaje: str, enumerado: type[Enum], actual: Enum) -> Enum:
    opciones = list(enumerado)
    for indice, opcion in enumerate(opciones, 1):
        print(f'{indice}. {opcion.name}')
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return actual
        try:
            numero = int(valor)
            if 1 <= numero <= len(opciones):
                return opciones[numero - 1]
        except ValueError:
            pass
        print('Opcion fuera de rango')
