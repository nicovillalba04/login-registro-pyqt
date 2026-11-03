from PyQt6.QtWidgets import QStackedWidget

from ventanas.ventana_login import VentanaLogin
from ventanas.ventana_registro import VentanaRegistro
from controladores.autenticacion import ServicioAutenticacion


class VentanaPrincipal(QStackedWidget):
    """La ventana de la aplicación: muestra una pantalla por vez."""

    def __init__(self):
        super().__init__()
        servicio = ServicioAutenticacion()
        self.login = VentanaLogin(servicio)
        self.registro = VentanaRegistro(servicio)
        self.addWidget(self.login)
        self.addWidget(self.registro)

        self.login.btn_ir_registro.clicked.connect(self.mostrar_registro)
        self.registro.btn_volver_login.clicked.connect(self.mostrar_login)

    def mostrar_login(self):
        self.setCurrentWidget(self.login)

    def mostrar_registro(self):
        self.setCurrentWidget(self.registro)
