# telegram_bot/bot_utils.py
import requests

TELEGRAM_TOKEN = '7480598750:AAGk3gjDP20qoGZmlwg7Xo1re2b3OOGl4Jk'
CHAT_ID = '1920633138'
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'


def send_message(chat_id, text):
    """
    Envía un mensaje al chat de Telegram.

    Este método utiliza la API de Telegram para enviar un mensaje al
    chat especificado por el ID.

    Parameters
    ----------
    chat_id : int
        El ID del chat al que se enviará el mensaje.
    text : str
        El texto del mensaje que se enviará.

    Returns
    -------
    dict
        Respuesta JSON de la API de Telegram con los detalles del mensaje enviado.
    """
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}

    print(
        f'Enviando mensaje a {chat_id}: {text}'
    )  # Esto ayudará a ver los datos que estás enviando

    response = requests.get(url, params=params)

    print(
        f'Respuesta de Telegram: {response.json()}'
    )  # Ver la respuesta completa para detectar errores

    return response.json()


def get_updates():
    """
    Obtiene los mensajes recientes que el bot ha recibido.

    Este método utiliza la API de Telegram para recuperar las actualizaciones
    (mensajes) que han sido enviados al bot.

    Returns
    -------
    dict
        Respuesta JSON de la API de Telegram con las actualizaciones recibidas.
    """
    url = BASE_URL + 'getUpdates'
    response = requests.get(url)
    return response.json()
