"""Servicio de autenticación SIMULADO, en memoria.

No es un sistema de producción: los usuarios se pierden al cerrar la app,
no hay límite de intentos, ni sesiones, ni base de datos.
Lo que sí hace bien desde ahora: nunca guarda la contraseña, solo su hash con sal.
"""
import hashlib
import hmac
import os

LONGITUD_MINIMA_PASSWORD = 8
ITERACIONES = 600_000


class ServicioAutenticacion:

    def __init__(self):
        # "ana@correo.com" -> {"nombre": ..., "apellido": ..., "sal": ..., "hash": ...}
        self._usuarios = {}

    def registrar(self, nombre, apellido, usuario, password):
        clave = usuario.strip().lower()
        minimo = LONGITUD_MINIMA_PASSWORD
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if not apellido.strip():
            raise ValueError("El apellido es obligatorio.")
        if not usuario.strip():
            raise ValueError("El nombre de usuario es obligatorio.")
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        if len(password) < minimo:
            raise ValueError(f"La contraseña necesita al menos {minimo} caracteres.")
        if clave in self._usuarios:
            raise ValueError("Ese usuario ya está registrado.")

        sal = os.urandom(16)
        self._usuarios[clave] = {
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "sal": sal,
            "hash": self._calcular_hash(password, sal),
        }

    def autenticar(self, usuario, password):
        """Verifica las credenciales del usuario.
        
        Devuelve True si son correctas, o False si el usuario no existe
        o la contraseña es incorrecta.
        """
        clave = usuario.strip().lower()

        # Buscamos el usuario. Si no existe, .get() devuelve None
        datos_usuario = self._usuarios.get(clave)
        if not datos_usuario:
            return False

        # Recalculamos el hash con la sal del usuario encontrado
        hash_calculado = self._calcular_hash(password, datos_usuario["sal"])

        # Comparación segura de los hashes
        if not hmac.compare_digest(datos_usuario["hash"], hash_calculado):
            return False

        return True

    @staticmethod
    def _calcular_hash(password, sal):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), sal, ITERACIONES
        )