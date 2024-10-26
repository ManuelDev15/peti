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

channel = -1002360088103
chann = "DevFast_FreeUp"

admins = {7346891727, 6181692448}
archived_messages = []

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)


################


@bot.message_handler(func=lambda message: message.chat.type == 'group')
def handle_message(message):
    if '#' in message.text:
        if '#peticion' in message.text:
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                msgn = f'<code>{msgo}</code>\n\n<b>✅Petición de:</b> @{username}'
                save = f"<b>Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, parse_mode='HTML')
                bot.reply_to(message, save, parse_mode='HTML')
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

###############

@bot.message_handler(commands=['reset'])
def resetarchiving(message):
    archived_messages.clear()
    bot.reply_to(message, "<b><i>Reset ejecutado</i></b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: True and not message.text.startswith('/') and message.chat.type == 'private')
def archive_message(message):
    user_id = message.from_user.id
    if user_id not in admins:
        return
    if message.chat.type == 'private':
        if archived_messages is not None:
            args = message.text.split("=")
            if len(args) == 2:
                arg0 = args[0]
                arg1 = args[1]
                forms = f"<a href='{arg1}'>{arg0} ⬅</a>"
                archived_messages.append("• " + f"<b>{forms}</b>")
                cmessage = "<b>📄Lista de peticiones subidas:</b>\n\n" + "\n".join(archived_messages) + "\n\n<b>/listo</b>"
                bot.reply_to(message, cmessage, parse_mode='HTML', disable_web_page_preview=True)

            else:
                bot.reply_to(message, "<b>Recuerda enviar el nombre, el signo igual (=) y después el link</b>", parse_mode='HTML')



@bot.message_handler(commands=['listo'])
def send_archived_messages(message):
    if archived_messages:
        combined_message = "<b>📄Lista de peticiones subidas:</b>\n\n" + "\n".join(archived_messages)
        msl = bot.send_message(channel, combined_message, parse_mode='HTML', disable_web_page_preview=True)
        
        meslink = f"https://t.me/{chann}/{msl.message_id}"
        linf = f"<a href='{meslink}'>Mensaje enviado al canal☑️</a>"
        listo = f"\n\n<b>{linf}</b>"
        bot.send_message(message.chat.id, listo, parse_mode='HTML', disable_web_page_preview=True)
        
        archived_messages.clear()
    else:
        bot.reply_to(message, "<i>No hay mensajes archivados</i>", parse_mode='HTML' )




### MAIN #######################
def run_server():
    PORT = 8029
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
