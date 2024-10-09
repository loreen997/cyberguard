from bot import MyClient
from detector import InsultoDetector

def main():
    # Crear una instancia del detector de insultos
    detector = InsultoDetector()

    # Crear una instancia del bot y pasarle el detector de insultos
    client = MyClient(detector)

    # Token del bot (debes pegar tu token aquí)
    TOKEN = 'MTI5MDgwNzU3MjM3NDM1NTk2OQ.GaP35R.G6D0L_KxM_tqMRQOztvB1YnVcp93dbC2PFOOUE'

    # Ejecutar el bot
    client.run(TOKEN)

if __name__ == "__main__":
    main()
