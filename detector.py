
from datetime import datetime
import os

def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")

    return fecha


intentos = {}


if not os.path.exists("eventos.log"):
    print("No existe el archivo eventos.log")
    exit()

# Leer los eventos registrados
with open("eventos.log", "r", encoding="utf-8") as archivo:

    for linea in archivo:

        partes = linea.strip().split(",", 2)

        if len(partes) != 3:
            continue

        fecha, tipo, usuario = [campo.strip() for campo in partes]

        if tipo == "LOGIN_FALLIDO":

            if usuario not in intentos:
                intentos[usuario] = []

            intentos[usuario].append(fecha)



tiempos_deteccion = []

for usuario, registros in intentos.items():

    if len(registros) >= 3:

        print("\n========== ALERTA DE SEGURIDAD ==========")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[2])

        inicio = datetime.strptime(
            registros[0], "%Y-%m-%d %H:%M:%S"
        )

        deteccion = datetime.strptime(
            registros[2], "%Y-%m-%d %H:%M:%S"
        )

        respuesta = datetime.strptime(
            fecha_respuesta,
            "%Y-%m-%d %H:%M:%S"
        )
        mttr = (respuesta - deteccion).total_seconds()
        print("MTTR:", mttr, "segundos")

        mttd = (deteccion - inicio).total_seconds()
        print("MTTD:", mttd, "scgundos")

        fecha_respuesta = registrar_respuesta(usuario)

        print("Acción aplicada: bloqueo registrado")
        print("Respuesta:", fecha_respuesta)
        print("MTTD:", mttd, "segundos")


if tiempos_deteccion:

    promedio = sum(tiempos_deteccion) / len(tiempos_deteccion)

    print("\n========== RESUMEN ==========")
    print("Usuarios detectados:", len(tiempos_deteccion))
    print("MTTD promedio:", round(promedio, 2), "segundos")

else:

    print("\nNo se detectaron usuarios con tres intentos fallidos.")
