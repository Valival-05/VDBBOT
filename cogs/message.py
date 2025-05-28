import discord
from discord.ext import commands

# Remplace avec ton token de bot
TOKEN = 'DISCORD_TOKEN'

intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire le contenu des messages

bot = commands.Bot(command_prefix='!', intents=intents)

class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='envoyer')
    async def envoyer(self, ctx, *, message: str):
        """Commande simple pour envoyer un message."""
        await ctx.send(message)

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user}')

async def setup():
    await bot.add_cog(MessageCommands(bot))

# Lancer le bot avec le chargement du Cog
async def main():
    await setup()
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
