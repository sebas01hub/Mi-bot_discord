import discord
from discord.ext import commands
import os
from modelo import machine

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents = intents)

TOKEN = "MTUzNTY3MTIyOTk2NzUwNzUwNg.GJAGEH.GWucnhXdYFfEV92mFeTBDP2aq76HBhGuw9Ajcc"

@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user}")

@bot.command()
async def hola(ctx):
    await ctx.send("Hola, ¿Como estas?")

@bot.command()
async def check(ctx):

    if not ctx.message.attachments:
        await ctx.send("No enviaste ninguna imagen.")
        return

    image = None

    for archivo in ctx.message.attachments:
        if archivo.content_type and archivo.content_type.startswith("image/"):
            image = archivo
            break

    if image is None:
        await ctx.send("El archivo enviado no es una imagen.")
        return

    os.makedirs("img", exist_ok=True)

    ruta = os.path.join("img", image.filename)

    await image.save(ruta)

    await ctx.send("Analizando imagen...")

    try:
        resultado, porcent = machine(ruta)

        porcentaje = porcent * 100

        await ctx.send(
            f"Resultado de la detección: {resultado}\n"
            f"Porcentaje: {porcentaje:.2f}%"
        )

    except Exception as e:
        print(f"Error al analizar la imagen: {e}")

        await ctx.send(
            "Ocurrió un error al analizar la imagen."
        )

bot.run(TOKEN)