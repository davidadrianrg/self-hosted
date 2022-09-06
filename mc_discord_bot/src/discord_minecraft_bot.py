# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
# IMPORT DOCKER ALLOWS TO CHECK DOCKER CONTAINERS INFORMATION
import docker

# IMPORT THE OS MODULE.
import os

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="/")

# CREATE A COMMAND TO SEE THE STATUS OF THE MINECRAFT SERVER (ONLINE/OFFLINE)
@bot.command()
async def status(ctx):
    docker_client = docker.from_env()
    mc_server = docker_client.get("minecraft")
    status_mc = mc_server.status()
    if status_mc == "running":
        response = "ONLINE"
    elif status_mc == "exited":
        response = "OFFLINE"
    else: response = "EN MANTENIMIENTO"
	await ctx.channel.send(f"El servidor de Minecraft está {response}")

# CREATE A COMMAND TO START THE MINECRAFT SERVER
@bot.command()
async def start(ctx):
    docker_client = docker.from_env()
    mc_server = docker_client.get("minecraft")
    status_mc = mc_server.status()
    if status_mc == "running":
        response = "El servidor de Minecraft ya está iniciado"
    elif status_mc == "exited":
        mc_server.start()
        response = "El servidor de Minecraft se está iniciando"
    else: response = "El servidor de Minecraft está en mantenimiento"
	await ctx.channel.send(response)

# CREATE A COMMAND TO STOP THE MINECRAFT SERVER
@bot.command()
async def stop(ctx):
    docker_client = docker.from_env()
    mc_server = docker_client.get("minecraft")
    status_mc = mc_server.status()
    if status_mc == "running":
        mc_server.stop()
        response = "El servidor de Minecraft se está apagando"
    elif status_mc == "exited":
        response = "El servidor de Minecraft ya está apagado"
    else: response = "El servidor de Minecraft está en mantenimiento"
	await ctx.channel.send(response)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(DISCORD_TOKEN)