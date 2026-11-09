
from flask import Flask, render_template, request # type: ignore
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from datetime import datetime

app = Flask(__name__)

# Conexion a la base de datos
def conectar_db():
    return sqlite3.connect("usuarios.db")


# Crear tabla si no existe
def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad -- Pimentel Marroquin --"


# Validar nombre de usuario
def validar_usuario(usuario):
    return re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario) is not None


# Validar correo electronico
def validar_correo(correo):
    return re.fullmatch(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        correo
    ) is not None


# Validar contrasena
def validar_password(password):
    return len(password) >= 8


# Registrar eventos de seguridad
def registrar_evento(tipo, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}, {tipo}, {usuario}\n")


# Registro de usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        if not validar_usuario(usuario):
            return "Usuario invalido: utiliza entre 4 y 20 caracteres."

        if not validar_correo(correo):
            return "Correo electronico invalido."

        if not validar_password(password):
            return "La contrasena debe contener al menos 8 caracteres."

        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
            (usuario, correo)
        )

        existente = cursor.fetchone()

        if existente:
            conexion.close()
            return "El usuario o correo ya esta registrado."

        password_hash = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
                (usuario, correo, password_hash)
            )

            conexion.commit()

        except sqlite3.Error as error:
            conexion.rollback()
            conexion.close()
            return f"Error al registrar usuario: {error}"

        conexion.close()

        registrar_evento("REGISTRO_CORRECTO", usuario)

        return "Usuario registrado correctamente."

    return render_template("registro.html")


# Inicio de sesion
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT password FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()
        conexion.close()

        if resultado and check_password_hash(resultado[0], password):

            registrar_evento("LOGIN_CORRECTO", usuario)

            return "Inicio de sesion correcto."

        else:

            registrar_evento("LOGIN_FALLIDO", usuario)

            return "Credenciales incorrectas."

    return render_template("login.html")


if __name__ == "__main__":

    inicializar_db()

    app.run(host="127.0.0.1", port=5000, debug=True)
