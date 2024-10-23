import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

from detector import InsultoDetector
from bbdd import guardar_mensaje, contar_mensajes_usuario, obtener_mensajes_usuario
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from Denuncia import enviar_denuncia

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
    diahora: str



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
            guardar_mensaje(autor, datetime.now(), "Discord", canal, contenido)

            # Contamos los mensajes ofensivos en la base de datos
            mensajes_guardados = contar_mensajes_usuario(autor)

            if mensajes_guardados >= 3:
                # Obtener los mensajes del usuario de la base de datos
                mensajes = obtener_mensajes_usuario(autor)

                # Enviar correo de denuncia
                email_destino = "denunciasrecibir@gmail.com"  # Dirección del administrador o moderador
                enviar_denuncia(email_destino, autor, mensajes)



                # Enviar notificación adicional de denuncia
                respuesta += (f"\nAdemás, ya has enviado {mensajes_guardados} mensajes ofensivos."
                              " Por lo tanto, has sido denunciado a los administradores del servidor.")

            # Reiniciar el contador después del tercer insulto
            usuarios_insultos[user_id] = 0

        # Devolver la respuesta privada y que el mensaje debe ser eliminado
        return respuesta, True

    else:
        # Si no es un insulto, reiniciamos el contador de insultos
        usuarios_insultos[user_id] = 0
        return None, False  # No enviar ninguna respuesta ni eliminar el mensaje
def context_mensaje(mensaje):
    
    mensaje_ia = {
        "messages": [
            {
                "role": "user",
                "content": "quiero que aceptes el rol para los mensajes que te aporte despues de --- y con formato autor:mensaje me interpretes lo que quieren decir para ayudar a una persona con problemas de socialización: ---" + mensaje #+ "Importante responde unicamente los mensajes absolutamente ningun texto mas"
            }
        ],
        "model": "unsloth/Llama-3.2-1B-Instruct-GGUF",
        "max_tokens": 2048,
        "stream": False,  
        "temperature": 0,
        "top_p": 1,
        "frequency_penalty": 0
    }


    response = requests.request("POST", "http://192.168.239.174:3000/v1/chat/completions", headers={'accept': 'text/event-stream' }, json=mensaje_ia)
    print(f"mensajes: {mensaje}")
    print(f"Response {response.json()}")
    mensaje_respuesta = response.json()



    return mensaje_respuesta['choices'][0]['message']['content'] 



@app.post("/procesar-mensaje/")
async def procesar_mensaje_api(message: Mensaje):
    """
    Endpoint para recibir y procesar un mensaje desde Discord.
    """
    respuesta, eliminar = procesar_mensaje(message)
    return {"respuesta": respuesta, "eliminar": eliminar}

@app.post("/context-mensaje/")
async def context_mensaje_api(message: str):
    """           
    Endpoint para recibir y contextualizar un mensaje desde Discord.
    """
    respuesta = context_mensaje(message)
    print(respuesta)
    return {"respuesta": respuesta}
 
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
