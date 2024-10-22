import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bbdd import contar_mensajes_usuario, obtener_mensajes_usuario


def enviar_denuncia(email_destino, autor, mensajes):
    """
    Envía un correo de denuncia con los mensajes de un usuario.

    :param email_destino: Dirección de correo donde se enviará la denuncia
    :param autor: Nombre del autor denunciado
    :param mensajes: Lista de mensajes ofensivos del autor
    """
    # Configuración del servidor SMTP (en este caso, usando Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'denunciaenviar@gmail.com'  # Cambia esto por tu correo de Gmail
    smtp_password = 'znka eckc hqeq pjuw'  # Cambia esto por tu contraseña de Gmail

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email_destino
    msg['Subject'] = f"Denuncia por comportamiento inapropiado de {autor}"

    # Crear el cuerpo del mensaje
    cuerpo = f"Se ha reportado al usuario {autor} por comportamiento inapropiado.\n\n"
    cuerpo += "Mensajes ofensivos:\n\n"

    for mensaje in mensajes:
        cuerpo += f"- {mensaje['diahora']}: {mensaje['mensaje']}\n"

    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        # Establecer conexión con el servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Protocolo TLS
        server.login(smtp_user, smtp_password)

        # Enviar el correo
        server.send_message(msg)
        server.quit()

        print(f"Correo de denuncia enviado a {email_destino} con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
