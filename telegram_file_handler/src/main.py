"""Telegram Bot to upload torrents  to watch folder."""
from telegram import Bot, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import os
from time import sleep
import logging
import zipfile
import rarfile

TOKEN = os.getenv('TELEGRAM_TOKEN')
WATCH_FOLDER = os.getenv('WATCH_FOLDER')
DOWNLOADS_FOLDER = os.getenv('DOWNLOADS_FOLDER')
#FILMS_FOLDER = os.getenv('FILMS_FOLDER')
USER_ID = int(os.getenv('TELEGRAM_USER_ID'))
bot = Bot(token=TOKEN)


def starter(update, context) -> None:
    update.message.reply_text(f'Hola! {update.effective_user.first_name}, Mandame el archivo torrent que quieras poner a descargar')


def torrent_downloader(update, context) :

    try:   
        message = update.message.reply_text("***Procesando...***")
        # Downloading file
        file_id = update.message.document.file_id  # Getting file id
        newFile = bot.get_file(file_id)
        
        fileName = update.message.document.file_name   # Getting filename
        
        # Downloading file directly in watch folder
        newFile.download(custom_path=os.path.join(WATCH_FOLDER,fileName))
        
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        message_id = message.message_id
        sleep(3)
        bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
        update.message.reply_text(f'Tu fichero se ha subido a la carpeta torrents')
    except Exception as e:
        print(e)    

def extract(update, context) -> None:
    message = update.message.reply_text("Extrayendo ficheros de la carpeta de descargas...")
    reply_message = "No se ha extraido ningún fichero"
    # Creating a list with all the files to be extracted
    subfolders = [f.path for f in os.scandir(os.path.join(DOWNLOADS_FOLDER, "complete")) if f.is_dir()]

    for sub in subfolders:
        for f in os.listdir(sub):
            src_file = os.path.join(sub, f)
            extension = f.split(".")[-1]
            logging.info(f"Checking to extract file: {src_file}")
            if extension == "zip":
                try:
                    with zipfile.ZipFile(src_file) as z:
                        for file in z.namelist():
                            if file.endswith(".avi") or file.endswith(".mkv") or file.endswith(".mp4"):
                                z.extract(file, path=os.path.join(DOWNLOADS_FOLDER, "extracted"))
                        logging.info(f"Extracted file {src_file}")
                    reply_message = "Ficheros extraidos satisfactoriamente" # In case that all go ok
                except Exception as e:
                    logging.error(f"Invalid file, error extracting: {e}")
                    reply_message = "Error extrayendo los archivos"
            if extension == "rar":
                try:
                    with rarfile.RarFile(src_file) as z:
                        for file in z.namelist():
                            f_endswith = file.split(".")[-1]
                            part_file = file.split(".")[-2]
                            if part_file.contains("part") and part_file != "part01": 
                                is_other_part = True
                            else: is_other_part = False
                            if f_endswith == "avi" or f_endswith == "mkv" or f_endswith == "mp4" and not is_other_part:
                                z.extract(file, path=os.path.join(DOWNLOADS_FOLDER, "extracted"))
                        logging.info(f"Extracted file {src_file}")
                    reply_message = "Ficheros extraidos satisfactoriamente" # In case that all go ok
                except Exception as e:
                    logging.error(f"Invalid file, error extracting: {e}")
                    reply_message = "Error extrayendo los archivos"
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
            message_id = message.message_id
            sleep(3)
            bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
            update.message.reply_text(reply_message)
            
       

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', starter, Filters.user(user_id=USER_ID)))
updater.dispatcher.add_handler(CommandHandler('extract', extract, Filters.user(user_id=USER_ID)))

updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, torrent_downloader))

updater.start_polling()
updater.idle()