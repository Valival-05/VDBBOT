import os
 from dotenv import load_dotenv
 import random
 import discord
 from discord.ext import commands
 import sys
 from keep_alive import keep_alive
 
 load_dotenv()
 
 token = os.getenv("DISCORD_TOKEN")
 bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())
 
 # L'événement on_ready
 @bot.event
 async def on_ready():
     print(f'Bot connecté en tant que {bot.user.name} ({bot.user.id})')
     channel = bot.get_channel(1358037453427966024)  # Remplace par l'ID du canal
     await channel.send("🎉 Je suis maintenant en ligne et prêt à vous aider ! 🎉")
 
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
