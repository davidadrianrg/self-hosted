# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
# IMPORT DOCKER ALLOWS TO CHECK DOCKER CONTAINERS INFORMATION
import docker

# IMPORT THE OS MODULE.
import os

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# IMPORT LOGGING TO LOG EXECUTION
import logging

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.AutoShardedBot(shard_count=1, command_prefix="$", intents=discord.Intents.default())

# CREATE A COMMAND TO SEE THE STATUS OF THE MINECRAFT SERVER (ONLINE/OFFLINE)
@bot.command()
async def status(ctx, game: str):
    docker_client = docker.from_env()
    try:
        game_server = docker_client.containers.get(game.lower())
        status_game = game_server.status
        logging.info(f"{game} server status obtained from docker socket: {status_game}")
    except Exception as e:
        status_game = "maintenance"
        logging.error(e)
    
    if status_game == "running":
        response = "ONLINE"
    elif status_game == "exited":
        response = "OFFLINE"
    else: response = "en mantenimiento"
    await ctx.channel.send(f"El servidor de {game} está {response}")

# CREATE A COMMAND TO START THE MINECRAFT SERVER
@bot.command()
async def start(ctx, game: str):
    docker_client = docker.from_env()
    try:
        game_server = docker_client.containers.get(game.lower())
        status_game = game_server.status
        logging.info(f"{game} server status obtained from docker socket: {status_game}")
    except Exception as e:
        status_game = "maintenance"
        logging.error(e)

    if status_game == "running":
        response = f"El servidor de {game} ya está iniciado"
    elif status_game == "exited":
        game_server.start()
        response = f"El servidor de {game} se está iniciando"
        logging.info(f"Starting {game} server docker container")
    else: response = f"El servidor de {game} está en mantenimiento"
    await ctx.channel.send(response)

# CREATE A COMMAND TO STOP THE MINECRAFT SERVER
@bot.command()
async def stop(ctx, game: str):
    docker_client = docker.from_env()
    try:
        game_server = docker_client.containers.get(game.lower())
        status_game = game_server.status
        logging.info(f"{game} server status obtained from docker socket: {status_game}")
    except Exception as e:
        status_game = "maintenance"
        logging.error(e)
    
    if status_game == "running":
        game_server.stop()
        response = f"El servidor de {game} se está apagando"
        logging.info(f"Stopping {game} server docker container")
    elif status_game == "exited":
        response = f"El servidor de {game} ya está apagado"
    else: response = f"El servidor de {game} está en mantenimiento"
    await ctx.channel.send(response)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(DISCORD_TOKEN)