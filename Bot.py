import discord
from discord import app_commands, client
from Servidor import procesar_mensaje
import os

# Configuración de intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.tree = app_commands.CommandTree(self)  # Crear árbol de comandos para slash commands

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')
        await self.tree.sync()  # Sincronizar los slash commands con el servidor
        print("Comandos slash sincronizados.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Procesamos el mensaje a través del servidor
        respuesta_privada, eliminar_mensaje = procesar_mensaje(message)

        if eliminar_mensaje:
            await message.delete()  # Eliminar el mensaje ofensivo del canal público
            await message.author.send(respuesta_privada)  # Enviar la advertencia por privado


# Definimos el comando slash /contexto
async def contexto(interaction: discord.Interaction, numero_de_mensajes: int):
    # Verificar que el número de mensajes sea válido
    if numero_de_mensajes <= 0:
        await interaction.response.send_message("Por favor, proporciona un número válido de mensajes.", ephemeral=True)
        return

    # Obtener los últimos 'numero_de_mensajes' del canal
    mensajes = await interaction.channel.history(limit=numero_de_mensajes).flatten()

    # Formatear los mensajes para enviarlos por privado
    contexto_mensajes = "\n\n".join([f"{msg.author.name}: {msg.content}" for msg in mensajes])

    # Enviar el contexto por mensaje privado
    await interaction.user.send(
        f"Aquí tienes los últimos {numero_de_mensajes} mensajes del canal:\n\n{contexto_mensajes}")

    # Confirmación de que el mensaje se ha enviado
    await interaction.response.send_message(f"Te he enviado los últimos {numero_de_mensajes} mensajes por privado.",
                                            ephemeral=True)


# Crear una instancia del bot y añadir el comando slash
client = MyClient()


def iniciar_bot():
    TOKEN = os.getenv('DISCORD_TOKEN', 'MTI5MDgwNzU3MjM3NDM1NTk2OQ.GaP35R.G6D0L_KxM_tqMRQOztvB1YnVcp93dbC2PFOOUE')
    client.run(TOKEN)
