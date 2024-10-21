import discord
from datetime import datetime
from collections import defaultdict
from bbdd import guardar_mensaje  # Asegúrate de que esta función esté implementada

# Configurar el intent para permitir la lectura de mensajes públicos y privados
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Necesario para leer el contenido de los mensajes


class MyClient(discord.Client):
    def __init__(self, detector=None, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.detector = detector  # El detector será opcional, solo en mensajes públicos

        # Diccionario que guarda cuántas veces ha insultado cada usuario
        self.usuarios_insultos = defaultdict(int)  # user_id: numero de insultos

    # Evento que se ejecuta cuando el bot está listo
    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

    # Evento que se ejecuta cada vez que un mensaje es enviado
    async def on_message(self, message):
        # Ignora los mensajes del propio bot
        if message.author == self.user:
            return

        # Detectar si el mensaje es público
        if not isinstance(message.channel, discord.DMChannel):
            autor = message.author.name
            contenido = message.content

            # Si tienes un detector de insultos para los mensajes públicos
            if self.detector:
                etiqueta, puntuacion = self.detector.detectar_insulto(contenido)
                print(f'Clasificación: {etiqueta} (Confianza: {puntuacion:.2f})')

                # Si se detecta un insulto
                if etiqueta == 'LABEL_1':  # Cambia 'LABEL_1' por la etiqueta correcta para insultos
                    await message.delete()  # Eliminar el mensaje inmediatamente

                    user_id = message.author.id  # ID del usuario que envió el mensaje
                    self.usuarios_insultos[user_id] += 1  # Aumentar el contador de insultos

                    # Obtener el número de veces que ha insultado
                    numero_de_insultos = self.usuarios_insultos[user_id]

                    if numero_de_insultos == 1:
                        # Primer insulto
                        await message.author.send(
                            f"Hola {autor}, hemos detectado que tu mensaje ( {contenido} ) en el canal #{message.channel.name} contenía un insulto.\n"
                            "Este tipo de comportamiento no está permitido. Por favor, evita usar lenguaje ofensivo."
                        )
                    elif numero_de_insultos == 2:
                        # Segundo insulto
                        await message.author.send(
                            f"Hola {autor}, este es tu segundo mensaje que contiene un insulto en el canal #{message.channel.name}.\n"
                            "Por favor, detén este comportamiento. De lo contrario, se podrían tomar acciones más severas."
                        )
                    elif numero_de_insultos == 3:
                        # Tercer insulto - Advertencia de denuncia
                        await message.author.send(
                            f"Hola {autor}, este es tu tercer mensaje con insultos detectado en el canal #{message.channel.name}.\n"
                            "Si continúas con este comportamiento, podrías ser denunciado por lenguaje inapropiado. Te pedimos que seas respetuoso."
                        )

                        # Guardar solo el tercer insulto en la base de datos
                        guardar_mensaje(autor,  datetime.now(), "Discord",  contenido  )
                        # Reiniciar el ciclo después del tercer insulto
                        self.usuarios_insultos[user_id] = 0

                else:
                    # Si el mensaje no es un insulto, reiniciar el contador de insultos
                    user_id = message.author.id
                    self.usuarios_insultos[user_id] = 0  # Reiniciar el contador si envía un mensaje normal
