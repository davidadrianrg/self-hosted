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
async def status(ctx):
    docker_client = docker.from_env()
    try:
        mc_server = docker_client.containers.get("minecraft")
        status_mc = mc_server.status()
        logging.info(f"Minecraft server status obtained from docker socket: {status_mc}")
    except Exception as e:
        status_mc = "maintenance"
        logging.error(e)
    
    if status_mc == "running":
        response = "ONLINE"
    elif status_mc == "exited":
        response = "OFFLINE"
    else: response = "en mantenimiento"
    await ctx.channel.send(f"El servidor de Minecraft está {response}")

# CREATE A COMMAND TO START THE MINECRAFT SERVER
@bot.command()
async def start(ctx):
    docker_client = docker.from_env()
    try:
        mc_server = docker_client.containers.get("minecraft")
        status_mc = mc_server.status()
        logging.info(f"Minecraft server status obtained from docker socket: {status_mc}")
    except Exception as e:
        status_mc = "maintenance"
        logging.error(e)

    if status_mc == "running":
        response = "El servidor de Minecraft ya está iniciado"
    elif status_mc == "exited":
        mc_server.start()
        response = "El servidor de Minecraft se está iniciando"
        logging.info("Starting Minecraft server docker container")
    else: response = "El servidor de Minecraft está en mantenimiento"
    await ctx.channel.send(response)

# CREATE A COMMAND TO STOP THE MINECRAFT SERVER
@bot.command()
async def stop(ctx):
    docker_client = docker.from_env()
    try:
        mc_server = docker_client.containers.get("minecraft")
        status_mc = mc_server.status()
        logging.info(f"Minecraft server status obtained from docker socket: {status_mc}")
    except Exception as e:
        status_mc = "maintenance"
        logging.error(e)
    
    if status_mc == "running":
        mc_server.stop()
        response = "El servidor de Minecraft se está apagando"
        logging.info("Stopping Minecraft server docker container")
    elif status_mc == "exited":
        response = "El servidor de Minecraft ya está apagado"
    else: response = "El servidor de Minecraft está en mantenimiento"
    await ctx.channel.send(response)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(DISCORD_TOKEN)