import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from detector import InsultoDetector
from bbdd import guardar_mensaje
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una instancia del detector
detector = InsultoDetector()

# Diccionario para llevar el control de los insultos por usuario
usuarios_insultos = {}

class Mensaje(BaseModel):
    autor: str  # Cambié de 'autor' a 'author' por consistencia con Discord.py
    user_id: int
    contenido: str
    canal: str



def procesar_mensaje(message):
    """
    Procesa el mensaje recibido desde Discord.
    - Detecta insultos.
    - Gestiona la respuesta.
    - Guarda en la base de datos si es necesario.
    """
    autor = message.autor
    user_id = message.user_id
    contenido = message.contenido
    canal = message.canal
    diahora = message.diahora

    # Detectamos si el mensaje contiene un insulto
    etiqueta, puntuacion = detector.detectar_insulto(contenido)
    print(f'Clasificación: {etiqueta} (Confianza: {puntuacion:.2f})')

    if etiqueta == 'LABEL_1':  # Cambia 'LABEL_1' por la etiqueta correcta de insultos
        # Incrementamos el contador de insultos del usuario
        if user_id not in usuarios_insultos:
            usuarios_insultos[user_id] = 0
        usuarios_insultos[user_id] += 1
        numero_de_insultos = usuarios_insultos[user_id]

        # Respuesta personalizada según el número de insultos
        if numero_de_insultos == 1:
            respuesta = (f"Hola {autor}, tu mensaje en el canal #{canal} contenía un insulto."
                         " Por favor, evita usar lenguaje ofensivo.")
        elif numero_de_insultos == 2:
            respuesta = (f"Hola {autor}, este es tu segundo insulto en el canal #{canal}."
                         " Por favor, detente o tomaremos acciones más serias.")
        elif numero_de_insultos == 3:
            respuesta = (f"Hola {autor}, este es tu tercer insulto en el canal #{canal}."
                         " Si continúas, podrías ser denunciado por comportamiento inapropiado.")

            # Guardamos el mensaje en la base de datos
            guardar_mensaje(autor, datetime.now(), "Discord", contenido)

            # Reiniciar el contador después del tercer insulto
            usuarios_insultos[user_id] = 0

        # Devolver la respuesta privada y que el mensaje debe ser eliminado
        return respuesta, True

    else:
        # Si no es un insulto, reiniciamos el contador de insultos
        usuarios_insultos[user_id] = 0
        return None, False  # No enviar ninguna respuesta ni eliminar el mensaje

@app.post("/procesar-mensaje/")
async def procesar_mensaje_api(message: Mensaje):
    """
    Endpoint para recibir y procesar un mensaje desde Discord.
    """
    respuesta, eliminar = procesar_mensaje(message)
    return {"respuesta": respuesta, "eliminar": eliminar}

@app.get("/estado/")
async def estado():
    """
    Endpoint para obtener el estado del servidor.
    """
    return {"estado": "Servidor en línea y funcionando correctamente"}

def iniciar_servidor():
    """
    Inicia el servidor FastAPI.
    """
    import uvicorn
    print("Servidor FastAPI iniciado y listo para recibir mensajes.")
    uvicorn.run(app, host="127.0.0.1", port=8000)
