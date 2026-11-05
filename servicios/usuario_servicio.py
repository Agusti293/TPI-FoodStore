from entidades.usuario import Usuario
from enums import Rol
from excepciones import (CredencialesInvalidasError, DuplicadoError,
                         EntidadNoEncontradaError, OperacionNoPermitidaError, FoodStoreError)


class UsuarioServicio:
    __usuarios: list[Usuario]

    def __init__(self) -> None:
        self.__usuarios = []

    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self, identificador: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == identificador and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError('Usuario no encontrado')

    def crear(self, nombre: str, apellido: str, mail: str, celular: str,
              contrasenia: str, rol: Rol) -> Usuario:
        self.__validar_mail_unico(mail)
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(usuario)
        return usuario

    def editar(self, identificador: int, nombre: str, apellido: str, mail: str,
               celular: str, contrasenia: str, rol: Rol) -> Usuario:
        usuario = self.buscar_por_id(identificador)
        if mail.strip().lower() != usuario.mail:
            self.__validar_mail_unico(mail)
        anteriores: tuple[str, str, str, str, Rol] = (
            usuario.nombre, usuario.apellido, usuario.mail, usuario.celular, usuario.rol
        )
        try:
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.mail = mail
            usuario.celular = celular
            usuario.rol = rol
            if contrasenia:
                usuario.cambiar_contrasenia(contrasenia)
        except (FoodStoreError, ValueError, TypeError):
            usuario.nombre, usuario.apellido, usuario.mail, usuario.celular, usuario.rol = anteriores
            raise
        return usuario

    def eliminar(self, identificador: int, sesion: Usuario) -> None:
        usuario = self.buscar_por_id(identificador)
        if usuario == sesion:
            raise OperacionNoPermitidaError('No puede eliminarse el administrador con sesion iniciada')
        usuario.eliminado = True

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for usuario in self.__usuarios:
            if (usuario.mail == mail.strip().lower() and not usuario.eliminado and
                    usuario.verificar_contrasenia(contrasenia)):
                return usuario
        raise CredencialesInvalidasError('Mail o contrasenia incorrectos')

    def __validar_mail_unico(self, mail: str) -> None:
        if any(u.mail == mail.strip().lower() for u in self.__usuarios):
            raise DuplicadoError('Ya existe un usuario con ese mail')
