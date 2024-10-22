import discord
from discord import app_commands
from Servidor import procesar_mensaje
import os


# Configuración de intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Lista local para almacenar los mensajes privados (DMs)
mensajes_privados = []


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

        # Si el mensaje es por privado (DM), lo almacenamos en la lista local en vez de en la base de datos
        if isinstance(message.channel, discord.DMChannel):
            # Guardar el mensaje en la lista local
            mensaje_info = {
                'autor': message.author.name,
                'user_id': message.user_id,
                'contenido': message.content,
                'canal': message.chanel,
                'diahora': message.created_at

            }
            mensajes_privados.append(mensaje_info)
            print(f"Mensaje privado recibido y almacenado: {mensaje_info}")
            return

        # Procesar el mensaje en los canales públicos
        respuesta_privada, eliminar_mensaje = procesar_mensaje(mensaje_info)

        if eliminar_mensaje:
            await message.delete()  # Eliminar el mensaje ofensivo del canal público
            await message.author.send(respuesta_privada)  # Enviar la advertencia por privado


# Crear una instancia del bot y añadir el comando slash
client = MyClient()



########################################################################################################################
#                                                           GRAMATICA DE /CONTEXTO
# Añadimos el comando al árbol de comandos del bot
@client.tree.command(name="contexto", description="Obtén los últimos mensajes del canal.")
async def contexto(interaction: discord.Interaction, numero_de_mensajes: int):
    # Defiere la respuesta de la interacción para evitar que expire
    await interaction.response.defer(ephemeral=True)

    # Verificar que el número de mensajes sea válido
    if numero_de_mensajes <= 0:
        return

    # Obtener los últimos 'numero_de_mensajes' del canal
    mensajes = [msg async for msg in interaction.channel.history(limit=numero_de_mensajes)]

    # Formatear los mensajes para enviarlos por privado
    contexto_mensajes = "\n\n".join([f"{msg.author.name}: {msg.content}" for msg in mensajes])

    # Enviar el contexto por mensaje privado
    await interaction.user.send(
        f"Aquí tienes los últimos {numero_de_mensajes} mensajes del canal:\n\n{contexto_mensajes}")

    # Eliminar el mensaje que invocó el comando en el canal principal sin dejar rastro
    if interaction.message:
        await interaction.message.delete()

########################################################################################################################

def iniciar_bot():
    TOKEN = os.getenv('DISCORD_TOKEN', 'MTI5MDgwNzU3MjM3NDM1NTk2OQ.GaP35R.G6D0L_KxM_tqMRQOztvB1YnVcp93dbC2PFOOUE')
    client.run(TOKEN)
