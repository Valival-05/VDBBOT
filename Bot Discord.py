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
    print(f"[DEBUG] Bot connecté en tant que {bot.user.name} ({bot.user.id})")

    try:
        channel = await bot.fetch_channel(1353147720864501764)
        print(f"[DEBUG] Canal trouvé : {channel.name}")

        await channel.send("🎉 Je suis maintenant en ligne et prêt à vous aider ! 🎉")
        await asyncio.sleep(1)

        await channel.send("Je suis en train de démarrer ...")
        await asyncio.sleep(1)

        await channel.send("Les LOG ne sont pas encore disponibles.")
    
    except Exception as e:
        print(f"[ERREUR] Impossible d'envoyer le message : {e}")

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
