import telebot
from telebot import types
import threading
import http.server
import socketserver
import re
import time

API_TOKEN = '7764656259:AAF_7mPJUHp7egPMxnINjk0FMjgyu4q8Rbs'
bot = telebot.TeleBot(API_TOKEN)
idgroup = -1002369751844

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if '#' in message.text:
        if '#peticion' in message.text:
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                msgn = f'<code>{msgo}</code>\n\n<b>✅Petición de:</b> @{username}'
                bot.send_message(idgroup, msgn, parse_mode='HTML')
            else:
                ID = message.from_user.id
                msgo = message.text[10:]
                msgn = f'<code>{msgo}</code>\n\n<b>✅Petición de:</b> <a href="tg://openmessage?user_id={ID}">ID:{ID}</a>'
                bot.send_message(idgroup, msgn, parse_mode='HTML')
        else:
            ms = "<b>☝🏻🤓Las peticiones son de esta forma:</b>\n\n<code>#peticion *y aquí inserta la petición*</code>\n\n<i>•Solo así se guardará en el bot•</i>"

            try:
                eli = bot.reply_to(message, ms, parse_mode='HTML')
                threading.Thread(target=delete_message, args=(message.chat.id, eli.message_id, 15)).start()
            except Exception as e:
                print(f"Error al enviar mensaje informativo:\n{e}")

### MAIN #######################
def run_server():
    PORT = 8028
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

####################

def recibir_mensajes():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Error en el polling: {e}")
            time.sleep(15)  # Esperar 15 segundos antes de intentar nuevamente

####################

if __name__ == '__main__':
    # Crea un hilo para ejecutar la función run_server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()  # Inicia el hilo

    print('Iniciando el bot...')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    
    print('Bot Iniciado✓')
    print("--------------------------------")
