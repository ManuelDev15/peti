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
'l':'Enviar el link del mensaje al Canal',
'lc':'Salir de un grupo',
'f': 'Fijar un mensaje citandolo',
'com': 'Información sobre los comandos disponibles para admins(este mensaje)'}
version = "0.7.0"

god = 6181692448
admins = {7346891727, 6181692448, 1142828252, 5463723604, 7372906088}
usersban = {6874274574,}
curiosos = []
archived_messages = []

emoyis = ["🍓", "🌭", "🔥", "🕊", "🐳", "🌚", "⚡️", "☃️", "💯", "🍾", "🏆", "🗿", "👻", "👨‍💻", "🎃", "🎄", "💊", "🦄", "👌🏻", "🆒"]
cont = 1
start_time = datetime.now()
#####

grupo2 = -1002322607547
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            if m.chat.id == grupo2:
                return
            if m.from_user.id == 6181692448:
                return
            info = "@devfastpeticionbot • " + f"@{str(m.from_user.username)}" + " [" + str(m.from_user.id) + "]:\n" + m.text
            #print(info)
            if m.chat.type == 'private':
                bot.send_message(grupo2, info)
            
bot.set_update_listener(listener)

#######

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)

######

def teclado_inline(arte, mlink=0):
    
    teclado = types.InlineKeyboardMarkup()
    
    btn_linkbtn = types.InlineKeyboardButton("mensaje💬", url=mlink)
    btn_link = types.InlineKeyboardButton(">>> TOCA AQUÍ <<<", url="https://t.me/DevFast_FreeUp/22")
    #####
    if arte == "plink":
        teclado.add(btn_link)
    if arte == "linkb":
        teclado.row_width = 1
        teclado.add(btn_linkbtn)
    
    return teclado

#####

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userid = m.from_user.id
    username = m.from_user.username
    if m.chat.type == 'private':
        if userid == god:
            bot.send_message(god, "<b>Un placer verle Sr. KatSIN3D♥️🗿</b>")
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

@bot.message_handler(commands=['l'])
def msendlink(m):
    if m.from_user.id not in admins:
        return
    msend = "<b>¿Cómo hacer una petición🤔?</b>"
    bot.send_message(channel, msend, reply_markup=teclado_inline('plink'))
    bot.send_message(m.chat.id, "<b>Mensaje enviado correctamente al canal✅</b>")

#######

@bot.message_handler(commands=['lc'])
def salirgroup(message):
    if message.from_user.id not in admins:
        return
    mssg = message.text.split(" ")
    if len(mssg) > 1:
        if len(mssg) > 2:
            bot.send_message(message.chat.id, "▎<b>Comando mal ejecutado</b>")
        else:
            if not mssg[1].isdigit():
                bot.send_message(message.chat.id, "▎<b>error, el id son solamente números</b>")
            else:
                bot.send_message(message.chat.id, "▎<i>procesando...</i>")
                id = f"-100{mssg[1]}"
                salirg(message, id)
    else:
        bot.send_message(message.chat.id, "▎<b>Es /lc -id del grupo-</b>")

def salirg(message, id):
    bot.leave_chat(id)
    bot.send_message(message.chat.id, "▎Listo")

######

@bot.message_handler(commands=['f'])
def pin_message(message):
    if message.from_user.id not in admins:
        return
    if message.reply_to_message:
        chat_id = message.chat.id
        message_id = message.reply_to_message.message_id
        
        try:
            bot.pin_chat_message(chat_id, message_id, disable_notification=True)
            threading.Thread(target=delete_message, args=(message.chat.id, message.message_id, 0)).start()
            
            mes_id = message.message_id + 1
            bot.delete_message(message.chat.id, mes_id)
        except Exception as e:
            bot.reply_to(message, f"<b>❌Error al anclar el mensaje:</b>\n\n{e}")
            print(e)
    else:
        bot.reply_to(message, "<b>⚠️Responde a un mensaje para anclarlo</b>")

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
    versionm = f"<b>▎<i>version: </i>{version}</b>"
    reac = bot.send_message(message.chat.id, versionm)
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
    global cont
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

    
    if "jey" in message.text.lower():
        if cont == 1:
            bot.reply_to(message, "🏳️‍🌈")
            cont += 1
        elif cont == 2:
            bot.reply_to(message, "🏳️‍🌈")
            cont += 1
        elif cont == 3:
            bot.reply_to(message, "🏳️‍🌈")
            cont += 1
        elif cont == 4:
            cont += 1
        else:
            cont = 1
        return
    if message.from_user.id in usersban:
        return
    if message.text.lower() == "hi" or message.text.lower() == "hola":
        bot.send_message(message.chat.id, "<b>Hola!</b>")
        return

#####################
 
    if message.text.startswith('#'):
        namet = message.from_user.first_name
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
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[12:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>{namet}</a> [<code>{ID}</code>]"
                save = f"<b>▎Petición archivada📦</b>"
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
                
                
        elif '#peticion' in message.text:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emoyis))])
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f'<code>{msgo}</code>\n\n<b>▎Petición de:</b> @{username}'
                save = f"<b>▎Petición archivada📦</b>"
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>{namet}</a> [<code>{ID}</code>]"
                save = f"<b>▎Petición archivada📦</b>"
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
                
        elif '#petición' in message.text:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emoyis))])
            if message.from_user.username is not None:
                username = message.from_user.username
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f'<code>{msgo}</code>\n\n<b>▎Petición de:</b> @{username}'
                save = f"<b>▎Petición archivada📦</b>"
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
            else:
                ID = message.from_user.id
                msgo = message.text[10:]
                mlink = f"https://t.me/{group}/{message.message_id}"
                msgn = f"<code>{msgo} </code>\n\n<b>▎Petición de:</b> <a href='tg://openmessage?user_id={ID}'>{namet}</a> [<code>{ID}</code>]"
                save = f"<b>▎Petición archivada📦</b>"
                idm = bot.send_message(idgroup, msgn, disable_web_page_preview=True, reply_markup=teclado_inline("linkb", mlink))
                
                bot.pin_chat_message(idgroup, idm.message_id, disable_notification=True)
                mes_id = idm.message_id + 1
                bot.delete_message(idgroup, mes_id)
                bot.reply_to(message, save)
            
        else:
            ms = "<b>▎☝🏻🤓Las peticiones son de esta forma:</b>\n<pre>#petición *y aquí inserta la petición*</pre>\n<pre>#peticion *y aquí inserta la petición*</pre>\n<pre>#peticiones *y aquí inserta la petición*</pre>\n<i>   • Solo así se guardarán las peticiones •</i>"
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji("✍")])

            try:
                eli = bot.reply_to(message, ms)
                threading.Thread(target=delete_message, args=(message.chat.id, eli.message_id, 20)).start()
            except Exception as e:
                bot.send_message(god, f"<b>❌Error al enviar mensaje informativo:</b>\n\n{e}")
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
    print("\033[32mBot Iniciado✓\033[0m")
    print(f"version: {version}")
    print("--------------------------------")
