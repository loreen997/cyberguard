from detector import InsultoDetector
from bbdd import guardar_mensaje
from datetime import datetime

# Crear una instancia del detector
detector = InsultoDetector()

# Diccionario para llevar el control de los insultos por usuario
usuarios_insultos = {}

def procesar_mensaje(message):
    """
    Procesa el mensaje recibido desde el bot.
    - Detecta insultos.
    - Gestiona la respuesta.
    - Guarda en la base de datos si es necesario.
    """

    autor = message.author.name
    user_id = message.author.id
    contenido = message.content

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
            respuesta = (f"Hola {autor}, tu mensaje en el canal #{message.channel.name} contenía un insulto."
                         " Por favor, evita usar lenguaje ofensivo.")
        elif numero_de_insultos == 2:
            respuesta = (f"Hola {autor}, este es tu segundo insulto en el canal #{message.channel.name}."
                         " Por favor, detente o tomaremos acciones más serias.")
        elif numero_de_insultos == 3:
            respuesta = (f"Hola {autor}, este es tu tercer insulto en el canal #{message.channel.name}."
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

def iniciar_servidor():
    print("Servidor iniciado y listo para recibir mensajes.")
    # Aquí podrías poner lógica adicional si lo deseas.
