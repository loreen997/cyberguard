from Bot import iniciar_bot
from Servidor import iniciar_servidor

import threading

def main():
    # Iniciar el servidor en un hilo separado
    servidor_hilo = threading.Thread(target=iniciar_servidor)
    servidor_hilo.start()

    # Iniciar el bot en el hilo principal
    iniciar_bot()


if __name__ == "__main__":
    main()
