from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit, QWidget
from controladores.autenticacion import LONGITUD_MINIMA_PASSWORD

RUTA_UI = Path(__file__).parent / "registro.ui"


class VentanaRegistro(QWidget):
    """Controla la pantalla de registro. El diseño vive en registro.ui."""

    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        uic.loadUi(RUTA_UI, self)
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.btn_registrar.clicked.connect(self.registrar)
        self.chk_mostrar_password.toggled.connect(self.alternar_password)


    def registrar(self):
        datos = self._leer_formulario()
        error = self._validar(datos)
        if error:
            self._mostrar_mensaje(error, "error")
            return
        try:
            self.servicio.registrar(datos["nombre"], datos["apellido"],
                            datos["usuario"], datos["password"])
        except ValueError as error:
            self._mostrar_mensaje(str(error), "error")
            return

        self._mostrar_mensaje("Cuenta creada. Ya podés volver e iniciar sesión.", "exito")

    def _leer_formulario(self):
        return {
        "nombre": self.input_nombre.text().strip(),
        "apellido": self.input_apellido.text().strip(),
        "usuario" : self.input_usuario.text().strip(),
        "password": self.input_password.text(),
        "confirmacion": self.input_confirmar_password.text(),
        }

    def _validar(self, datos):
        # 1. Validar campos obligatorios vacíos
        if not datos["nombre"]:
            return "El nombre es obligatorio."
        if not datos["apellido"]:
            return "El apellido es obligatorio."
        if not datos["usuario"]:
            return "El nombre de usuario es obligatorio."
        if not datos["password"]:
            return "La contraseña es obligatoria."

        # 2. Validar restricciones de longitud
        if len(datos["password"]) < LONGITUD_MINIMA_PASSWORD:
            return f"La contraseña debe tener al menos {LONGITUD_MINIMA_PASSWORD} caracteres."

        # 3. Validar coincidencia de contraseñas
        if datos["password"] != datos["confirmacion"]:
            return "Las contraseñas no coinciden."

        return None

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)

    def alternar_password(self, visible):
        if visible:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.input_confirmar_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.input_confirmar_password.setEchoMode(QLineEdit.EchoMode.Password)