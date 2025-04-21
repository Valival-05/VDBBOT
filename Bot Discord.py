import os
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
import sys
import asyncio
from keep_alive import keep_alive

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("[DEBUG] Je suis dans on_ready()")

@bot.command(help="Affiche un mot nommé Pong !")
async def Ping(ctx):
    await ctx.send(f"Pong !")

@bot.command(help="Affiche un mot te disant bonjour !")
async def bonjour(ctx):
    await ctx.send(f"Salut ! Je suis un bot. {ctx.author.name} !")

@bot.command(help="Affiche un mot aléatoire entre Pile et Face")
async def Aléatoire(ctx):
    await ctx.send(random.choice(["Pile !", "Face !"]))

keep_alive()
bot.run(token)
