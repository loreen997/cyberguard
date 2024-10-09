import psycopg2
import os

# Obtén la URL de la base de datos desde una variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://system:manager@localhost:5432/postgres')

# Conéctate a la base de datos PostgreSQL usando psycopg2
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            autor TEXT NOT NULL,
            diahora TIMESTAMP NOT NULL,
            plataforma TEXT NOT NULL,
            mensaje TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Función para guardar un mensaje
    def guardar_mensaje(autor, diahora, plataforma, mensaje):
        formato_fecha_hora = diahora.strftime('%Y-%m-%d %H:%M:%S')  # Convertir a string en formato DATETIME

        cursor.execute('''
                INSERT INTO mensajes (autor, diahora, plataforma, mensaje) 
                VALUES (%s, %s, %s, %s)
            ''', (autor, formato_fecha_hora, plataforma, mensaje))

        conn.commit()
        print(f'Mensaje guardado: {mensaje}')

    # Ejemplo de cómo usar la función
    #guardar_mensaje("Hola, este es un mensaje guardado en PostgreSQL!")

except Exception as e:
    print(f'Error al conectar a la base de datos: {e}')


# finally:
#     # Cerrar la conexión (si fuera necesario)
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()