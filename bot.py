import discord
from datetime import datetime
from bbdd import guardar_mensaje  # Importa la función para guardar mensajes

# Configurar el intent para permitir la lectura de mensajes
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Necesario para leer el contenido de los mensajes

# Lista para almacenar los mensajes
mensajes = []

class MyClient(discord.Client):
    def __init__(self, detector, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.detector = detector

    # Evento que se ejecuta cuando el bot está listo
    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

    # Evento que se ejecuta cada vez que un mensaje es enviado a un canal
    async def on_message(self, message):
        # Ignora los mensajes del propio bot
        if message.author == self.user:
            return

        # Obtén la información deseada
        autor = message.author.name  # Nombre del autor
        canal = message.channel.name  # Nombre del canal
        hora = datetime.now()  # Hora actual en formato datetime

        # Agrega el contenido del mensaje y la información adicional a la lista
        mensajes.append({
            "contenido": message.content,
            "autor": autor,
            "canal": canal,
            "hora": hora.strftime("%Y-%m-%d %H:%M:%S")
        })

        # Imprime la información en la consola
        print(f"Nuevo mensaje de {autor} en #{canal} a las {hora}: {message.content}")
        print(f"Total mensajes guardados: {len(mensajes)}")

        # Detectar insultos en el mensaje usando el detector de insultos
        etiqueta, puntuacion = self.detector.detectar_insulto(message.content)
        print(f'Clasificación: {etiqueta} (Confianza: {puntuacion:.2f})')

        # Si se detecta un insulto, guardarlo en la base de datos
        if etiqueta == 'LABEL_1':  # Cambia 'LABEL_1' por la etiqueta que use tu modelo para insultos
            # Guardar el mensaje en la base de datos
            guardar_mensaje(
                autor,               # Autor del mensaje
                hora,                # Fecha y hora actual
                "Discord",           # Plataforma (en este caso, Discord)
                message.content      # Contenido del mensaje
            )


