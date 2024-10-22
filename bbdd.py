import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://system:manager@localhost:5432/postgres')

# Conexión a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            autor TEXT NOT NULL,
            diahora TIMESTAMP NOT NULL,
            plataforma TEXT NOT NULL,
            canal TEXT NOT  NULL,
            mensaje TEXT NOT NULL
        )
    ''')
    conn.commit()

    def guardar_mensaje(autor, diahora, plataforma, canal, mensaje):
        formato_fecha_hora = diahora.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
                INSERT INTO mensajes (autor, diahora, plataforma,canal, mensaje) 
                VALUES (%s, %s, %s,%s, %s)
            ''', (autor, formato_fecha_hora, plataforma, canal, mensaje))
        conn.commit()
        print(f'Mensaje guardado en la base de datos: {mensaje}')



except Exception as e:
    print(f'Error al conectar a la base de datos: {e}')


def contar_mensajes_usuario(autor):
    cursor.execute('''
        SELECT COUNT(*) FROM mensajes WHERE autor = %s
    ''', (autor,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else 0