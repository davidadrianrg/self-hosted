"""Telegram Bot to upload torrents  to watch folder."""
from telegram import Bot, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import os
from time import sleep
import logging
import zipfile
import rarfile
import requests
import shutil
import json

# To develop in local without docker
#from dotenv import load_dotenv
#load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
WATCH_FOLDER = os.getenv('WATCH_FOLDER')
DOWNLOADS_FOLDER = os.getenv('DOWNLOADS_FOLDER')
FILMS_FOLDER = os.getenv('FILMS_FOLDER')
SERIES_FOLDER = os.getenv('SERIES_FOLDER')
IMDB_TOKEN = os.getenv('IMDB_TOKEN')
USER_ID = int(os.getenv('TELEGRAM_USER_ID'))
bot = Bot(token=TOKEN)

#Setting Logger
# Gets or creates a logger
logger = logging.getLogger(__name__)

# Set log level
logger.setLevel(logging.DEBUG)

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

def extracter(update, context) -> None:
    message = update.message.reply_text("Extrayendo ficheros de la carpeta de descargas...")
    reply_message = "No se ha extraido ningún fichero"
    # Creating a list with all the files to be extracted
    subfolders = [f.path for f in os.scandir(os.path.join(DOWNLOADS_FOLDER, "complete")) if f.is_dir()]

    for sub in subfolders:
        for f in os.listdir(sub):
            src_file = os.path.join(sub, f)
            extension = f.split(".")[-1]
            part_file = f.split(".")[-2]
            if part_file.__contains__("part") and part_file != "part01": 
                is_other_part = True
            else: is_other_part = False
            logger.debug(f"Checking to extract file: {src_file}")
            if extension == "zip" and not is_other_part:
                try:
                    with zipfile.ZipFile(src_file) as z:
                        for file in z.namelist():
                            if file.endswith(".avi") or file.endswith(".mkv") or file.endswith(".mp4"):
                                z.extract(file, path=os.path.join(DOWNLOADS_FOLDER, "extracted"))
                        logger.debug(f"Extracted file {src_file}")
                    reply_message = "Ficheros extraidos satisfactoriamente" # In case that all go ok
                except Exception as e:
                    logger.error(f"Invalid file, error extracting: {e}")
                    reply_message = "Error extrayendo los archivos"
            if extension == "rar" and not is_other_part:
                try:
                    with rarfile.RarFile(src_file) as z:
                        for file in z.namelist():
                            f_endswith = file.split(".")[-1]
                            if f_endswith == "avi" or f_endswith == "mkv" or f_endswith == "mp4":
                                z.extract(file, path=os.path.join(DOWNLOADS_FOLDER, "extracted"))
                                reply_message = "Ficheros extraidos satisfactoriamente" # In case that all go ok
                                logger.debug(f"Extracted file {src_file}")
                            else: logger.debug(f"No se ha extraido el fichero: {src_file}")
                except Exception as e:
                    logger.error(f"Invalid file, error extracting: {e}")
                    reply_message = "Error extrayendo los archivos"
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    message_id = message.message_id
    sleep(3)
    bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
    update.message.reply_text(reply_message)

def cleaner(update, context) -> None:
    #Call firstly the extracter and classifier functions
    extracter(update, context)
    classifier(update, context)
    #Proceed to clean the directory
    message = update.message.reply_text("Limpiando carpeta de descargas...")
    remove_folder = os.path.join(WATCH_FOLDER, "complete")
    logger.debug(f"Limpiando carpeta de descargas en {remove_folder}")
    os.remove(remove_folder)
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    message_id = message.message_id
    sleep(3)
    bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
    update.message.reply_text("Carpeta de descargas vaciada")

def classifier(update, context) -> None:
    message = update.message.reply_text("Colocando cada fichero en su carpeta destino")
    reply_message = "No se ha clasificado ningún fichero"
    # Creating a list with all the files to be moved
    subfolders = [f.path for f in os.scandir(os.path.join(DOWNLOADS_FOLDER, "complete")) if f.is_dir()]
    subfolders.append([f.path for f in os.scandir(os.path.join(DOWNLOADS_FOLDER, "extracted")) if f.is_dir()])

    for sub in subfolders:
        for f in os.listdir(sub):
            src_file = os.path.join(sub, f)
            extension = f.split(".")[-1]
            
            if extension == "avi" or extension == "mkv" or extension == "mp4":
                logger.debug(f"Checking to extract file: {src_file}")
                try:
                    # Make an api call to imdb to know if a file is a film or a serie
                    file_type = api_classify(f)
                    if file_type == "Movie":
                        shutil.move(src_file, os.path.join(FILMS_FOLDER, f))
                        reply_message = "Ficheros clasificados con éxito"
                    elif file_type == "TVSeries":
                        shutil.move(src_file, os.path.join(SERIES_FOLDER, f))
                        reply_message = "Ficheros clasificados con éxito"
                    else: reply_message = "Al menos un fichero no ha podido clasificarse"
                    reply_message = "Ficheros clasificados con éxito"
                except Exception as e:
                    logger.error(f"Error classifying the file: {e}")
                    reply_message = "Error clasificando los archivos"
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    message_id = message.message_id
    sleep(3)
    bot.delete_message(chat_id=update.effective_message.chat_id, message_id= message_id) 
    update.message.reply_text(reply_message)


def api_classify(file_name):
    url = f"https://imdb-api.com/es/API/Search/{IMDB_TOKEN}/{file_name}"
    response = requests.request("GET", url, headers={}, data = {})
    search = json.loads(response.text.encode('utf8'))
    # Get the id of the film or serie
    id = search.get("results")[0].get("id")

    url_title = f"https://imdb-api.com/es/API/Title/{IMDB_TOKEN}/{id}"
    # Get more info about the film or serie
    response = requests.request("GET", url_title, headers={}, data = {})
    # Get if it is a Movie or a TVSeries
    file_type = json.loads(response.text.encode('utf8')).get("type")
    return file_type

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', starter, Filters.user(user_id=USER_ID)))
updater.dispatcher.add_handler(CommandHandler('extract', extracter, Filters.user(user_id=USER_ID)))
updater.dispatcher.add_handler(CommandHandler('clean', cleaner, Filters.user(user_id=USER_ID)))
updater.dispatcher.add_handler(CommandHandler('classify', classifier, Filters.user(user_id=USER_ID)))

updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, torrent_downloader))

updater.start_polling()
updater.idle()