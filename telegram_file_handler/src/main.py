"""Telegram Bot to upload torrents  to watch folder."""
from telegram import Bot, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from os import getenv, path
from time import sleep

TOKEN = getenv('TELEGRAM_TOKEN')
WATCH_FOLDER = getenv('WATCH_FOLDER')
USER_ID = getenv('TELEGRAM_USER_ID')
bot = Bot(token=TOKEN)


def starter(update, context) -> None:
    update.message.reply_text(f'Hola! {update.effective_user.first_name}, Mandame el archivo torrent que quieras poner a descargar')


def torrent_downloader(update, context) :

    try:   
        message = update.message.reply_text("***Procesando...***")
        #downloading file
        file_id = update.message.document.file_id  #getting file id
        newFile = bot.get_file(file_id)
        
        fileName = update.message.document.file_name   #getting filename
        
        #Downloading file directly in watch folder
        newFile.download(custom_path=path.join(WATCH_FOLDER,fileName))
        
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        message_id = message.message_id
        sleep(3)
        bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
        update.message.reply_text(f'Tu fichero se ha subido a la carpeta torrents')
    except Exception as e:
        print(e)    

       

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', starter), Filters.user(user_id=int(USER_ID)))

updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, torrent_downloader))

updater.start_polling()
updater.idle()