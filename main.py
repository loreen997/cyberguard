# from BotGrupo import MyClient
# from BotPrivado import MyClient
# from detector import InsultoDetector
#
# def main():
#     # Crear una instancia del detector de insultos
#     detector = InsultoDetector()
#
#     # Crear una instancia del bot y pasarle el detector de insultos
#     client = MyClient(detector)
#
#     # Token del bot (debes pegar tu token aquí)
#     TOKEN = 'MTI5MDgwNzU3MjM3NDM1NTk2OQ.GaP35R.G6D0L_KxM_tqMRQOztvB1YnVcp93dbC2PFOOUE'
#
#     # Ejecutar el bot
#     client.run(TOKEN)
#
# if __name__ == "__main__":
#     main()
# main.py
from Bot import MyClient  # Asegúrate de que apunte correctamente a tu archivo Bot.py
from detector import InsultoDetector  # Tu clase de detector de insultos

def main():
    # Crear una instancia del detector de insultos
    detector = InsultoDetector()

    # Crear una instancia del bot y pasarle el detector de insultos (opcional, solo para mensajes públicos)
    client = MyClient(detector=detector)  # Detector se aplica solo en públicos

    # Token del bot (debes pegar tu token aquí)
    TOKEN = 'MTI5MDgwNzU3MjM3NDM1NTk2OQ.GaP35R.G6D0L_KxM_tqMRQOztvB1YnVcp93dbC2PFOOUE'

    # Ejecutar el bot
    client.run(TOKEN)

if __name__ == "__main__":
    main()

