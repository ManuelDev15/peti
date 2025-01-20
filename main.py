import telebot
from telebot import types
import threading
import http.server
import socketserver
import re
import time
import random
from telebot.types import ReactionTypeEmoji
from datetime import datetime, timedelta

##########
API_TOKEN = '7764656259:AAF_7mPJUHp7egPMxnINjk0FMjgyu4q8Rbs'
bot = telebot.TeleBot(API_TOKEN, parse_mode="html")
PORT = 8029

idgroup = -1002369751844
groupp = -1002415776665
channel = -1002360088103
chann = "DevFast_FreeUp"
group = "DevFast_FreeUpChat"
#####
comandos = {
'i': 'Saber id de alguien (responder a un mensaje)',
'd': 'Hablar por el bot',
'add': 'Agregar un admin al bot',
't': 'Tiempo activo del bot',
'tb': 'Hora real del bot',
'v': 'Ver la versión del bot',
'com': 'Información sobre los comandos disponibles para admins(este mensaje)'}

god = 7346891727 #6181692448
admins = {7346891727, 6181692448, 1142828252, 5463723604, 7372906088}
usersban = {6874274574}
archived_messages = []

emoyis = ["🍓", "🌭", "🔥", "🕊", "🐳", "🌚", "⚡️", "☃️", "💯", "🍾", "🏆", "🗿", "👻", "👨‍💻", "🎃", "🎄", "💊", "🦄", "👌🏻", "🆒"]
start_time = datetime.now()
#####

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)

######

def teclado_inline(arte):
    global mlink
    
    teclado = types.InlineKeyboardMarkup()
    
    btn_linkbtn = types.InlineKeyboardButton("mensaje💬", url=mlink)
    
    #####
    if arte == "linkb":
        teclado.row_width = 1
        teclado.add(btn_linkbtn)
    
    return teclado


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    if call.data == "linkb":
        command_start(call.message)
    
#####

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userid = m.from_user.id
    username = m.from_user.username
    if m.chat.type == 'private':
        if userid == god:
            bot.send_message(god, "<b>Un placer verle Sr. BluSINED♥️🗿</b>")
            return
        if userid in admins:
            bot.send_message(cid, f"▎<b>Hola admin </b>@{username} ...")
            bot.send_message(god, f"▎@{username}")
            return
        if userid not in curiosos:
            curiosos.append(userid)
            bot.send_message(god, f"▎<code>{userid}</code>")
            bot.send_message(cid, "<b>Hola extraño🙂...</b>")
        else:
            bot.send_message(cid, "<b>Hola de nuevo, extraño🙂...</b>")
            bot.send_message(god, f"▎<code>{userid}</code> 🔄")

#####

@bot.message_handler(commands=['com'])
def comandoshelp(m):
    if m.from_user.id not in admins:
        return
    comm = "<pre><b>Los siguientes comandos están disponibles(admins):</b></pre>\n"
    for comando in comandos:
        comm += f"<b>▎/{comando}:</b> "
        comm += f"<b>  {comandos[comando]}</b>\n"
    bot.send_message(m.chat.id, comm)
    threading.Thread(target=delete_message, args=(m.chat.id, m.message_id, 0)).start()
    
######

@bot.message_handler(commands=['i'])
def sendmesid(m):
    if m.reply_to_message:
        userid = m.reply_to_message.from_user.id
        bot.send_message(m.chat.id, f"▎<b>Id:</b> <code>{userid}</code>")

#####

@bot.message_handler(commands=['d'])
def hablarxbot(m):
    if m.from_user.id not in admins:
        return
    if len(m.text.split()) < 2:
        threading.Thread(target=delete_message, args=(m.chat.id, m.message_id, 0)).start()
        return
    else:
        say = m.text[3:]
        if m.reply_to_message:
            repms = m.reply_to_message
            bot.reply_to(repms, say)
            threading.Thread(target=delete_message, args=(m.chat.id, m.message_id, 0)).start()
        else:
            bot.send_message(m.chat.id, say)
            threading.Thread(target=delete_message, args=(m.chat.id, m.message_id, 0)).start()

#####

@bot.message_handler(commands=['add'])
def addadmin(m):
    if m.from_user.id not in admins:
        return
    if len(m.text.split()) < 2:
        bot.send_message(m.chat.id, "▎Su uso es así: /add -id-")
    else:
        idadmin = int(m.text.split()[1])
        if idadmin not in admins:
            admins.add(idadmin)
            text = f"<b>▎Id: <code>{idadmin}</code> agregado</b>"
            text2 = f"<pre>Actualizar:</pre>\n<code>admins = {admins}</code>"
            if m.from_user.id == god:
                bot.send_message(god, text)
                bot.send_message(god, text2)
            else:
                bot.send_message(m.chat.id, text)
                bot.send_message(god, text)
                bot.send_message(god, text2)
        else:
            bot.send_message(m.chat.id, f"▎<b>El id: <code>{idadmin}</code>  ya es admin</b>")
        print(f"admins = {admins}")

#####

@bot.message_handler(commands=['t'])
def send_uptime(message):
    if message.from_user.id not in admins:
        return
    current_time = datetime.now()
    uptime = current_time - start_time
    
    days, seconds = uptime.days, uptime.seconds
    hours = seconds // 3600
    min = (seconds % 3600) // 60
    sec = seconds % 60
    text = "▎<b>He estado activo durante: </b>"
    if days == 0:
        upmessage = f"{text}<code>{hours}h, {min}m, {sec}s</code>"
        if hours == 0:
            upmessage = f"{text}<code>{min}m, {sec}s</code>"
            if min == 0:
                upmessage = f"{text}<code>{sec}s</code>"
    else:
        upmessage = f"{text}<code>{days}d, {hours}h, {min}m, {sec}s</code>"
    bot.send_message(message.chat.id, upmessage)
    threading.Thread(target=delete_message, args=(message.chat.id, message.message_id, 0)).start()
    
#### 

@bot.message_handler(commands=['tb'])
def send_uptime(message):
    if message.from_user.id not in admins:
        return
    current_time = datetime.now()
    curreh = current_time.hour
    currem = current_time.minute
    mm = "am"
    if curreh == 0:
        curreh = "12"
    if curreh > 12:
        curreh = curreh - 12
        mm = "pm"
    bot.send_message(message.chat.id, f"<b>▎Hora real del bot:</b> <code>{curreh}:{currem}</code> <b>{mm}</b>")
    threading.Thread(target=delete_message, args=(message.chat.id, message.message_id, 0)).start()

#####

@bot.message_handler(commands=['v'])
def sendmessactual(message):
    if message.from_user.id not in admins:
        return
    ver = "<b>▎<i>version:</i> 0.6.2</b>"
    reac = bot.send_message(message.chat.id, ver)
    threading.Thread(target=delete_message, args=(message.chat.id, message.message_id, 0)).start()
    #bot.set_message_reaction(message.chat.id, reac.id, [ReactionTypeEmoji(random.choice(emoyis))])

#######

@bot.message_handler(commands=['reset'])
def resetarchiving(message):
    if message.from_user.id not in admins:
        return
    archived_messages.clear()
    bot.send_message(message.chat.id, "<b><i>▎Reset en los mensajes archivados</i></b>")
    threading.Thread(target=delete_message, args=(message.chat.id, message.message_id, 0)).start()

#######

@bot.message_handler(commands=['listo'])
def send_archived_messages(message):
    if message.from_user.id not in admins:
        return
    if archived_messages:
        combined_message = "▎<b>📄Lista de peticiones subidas:</b>\n\n" + "\n".join(archived_messages)
        msl = bot.send_message(channel, combined_message, disable_web_page_preview=True)
        
        meslink = f"https://t.me/{chann}/{msl.message_id}"
        linf = f"<a href='{meslink}'>🔗Link</a>"
        listo = f"\n\n<b>▎Mensaje enviado al canal☑️\n\n--{linf}--</b>"
        bot.send_message(message.chat.id, listo, parse_mode='HTML', disable_web_page_preview=True)
        
        archived_messages.clear()
    else:
        noarch = bot.reply_to(message, "<i>No hay mensajes archivados</i>")
        threading.Thread(target=delete_message, args=(message.chat.id, noarch.message_id, 10)).start()

#########

@bot.message_handler(func=lambda message: True and not message.text.startswith('/'))
def archive_message(message):
    if message.chat.type == 'private':
        if message.from_user.id not in admins:
            userid = message.from_user.id
            bot.send_message(god, f"{message.text}\n▎\n▎<code>{userid}</code>")
            return
        if archived_messages is not None:
            args = message.text.split("=")
            if len(args) == 2:
                arg0 = args[0]
                arg1 = args[1]
                forms = f"<a href='{arg1}'>{arg0} ⬅</a>"
                archived_messages.append("• " + f"<b>{forms}</b>")
                cmessage = "<pre>📄Lista de peticiones subidas:</pre>\n\n" + "\n".join(archived_messages) + "\n\n<b>/listo</b>"
                bot.reply_to(message, cmessage, disable_web_page_preview=True)
            else:
                reme = bot.reply_to(message, "▎<b>Recuerda enviar el nombre, el signo igual (=) y después el link</b>")
                threading.Thread(target=delete_message, args=(message.chat.id, reme.message_id, 10)).start()


    if message.from_user.id in usersban:
        return
    if message.text.lower() == "hi" or message.text.lower() == "hola":
        bot.send_message(message.chat.id, "<b>Hola!</b>")
        return

#####################
 
    if message.text.startswith('#'):
        if message.chat.id != groupp:
            return
        global mlink
        if '#peticiones' in message.text:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emoyis))])
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[12:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f'<code>{msgo}</code>\n\n<b>▎Petición de:</b> @{username}'
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[12:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>ID: {ID}</a>"
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
                
        elif '#peticion' in message.text:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emoyis))])
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f'<code>{msgo}</code>\n\n<b>▎Petición de:</b> @{username}'
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>ID: {ID}</a>"
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
                
        elif '#petición' in message.text:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emoyis))])
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f'<code>{msgo}</code>\n\n<b>▎Petición de:</b> @{username}'
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>ID: {ID}</a>"
                save = f"<b>▎Petición archivada📦</b>"
                bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb"))
                bot.reply_to(message, save)
            
        else:
            ms = "<b>▎☝🏻🤓Las peticiones son de esta forma:</b>\n<pre>#petición *y aquí inserta la petición*</pre>\n<pre>#peticion *y aquí inserta la petición*</pre>\n<pre>#peticiones *y aquí inserta la petición*</pre>\n<i>   • Solo así se guardarán las peticiones •</i>"
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji("✍")])

            try:
                eli = bot.reply_to(message, ms)
                threading.Thread(target=delete_message, args=(message.chat.id, eli.message_id, 20)).start()
            except Exception as e:
                print(f"Error al enviar mensaje informativo:\n\n{e}")


### MAIN #######################
def run_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port: {PORT}")
        httpd.serve_forever()

####################

def recibir_mensajes():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Error en el polling:\n{e}")
            time.sleep(15)  # Esperar 15 segundos antes de intentar nuevamente

####################
if __name__ == '__main__':
    print('Iniciando el bot...')
    # Crea un hilo para ejecutar la función run_server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()  # Inicia el hilo

    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print('Bot Iniciado✓')
    print("--------------------------------")
