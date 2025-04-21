import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class MonBot(commands.Bot):
    async def setup_hook(self):
        # Charge les extensions (cogs)
        for extension in ['games', 'moderation']:
            await self.load_extension(f'cogs.{extension}')
        
        # Synchronisation des commandes slash après avoir chargé les cogs
        await self.tree.sync()

    async def on_ready(self):
        print(f'Bot connecté en tant que {self.user}')

        statuses = [
            discord.Game("GorillaTAG"),
            discord.Activity(type=discord.ActivityType.watching, name="la description du BOT"),
            discord.Activity(type=discord.ActivityType.listening, name="de la musique")
        ]

        async def status_cycle():
            while True:
                for status in statuses:
                    print(f"[DEBUG] Changement de statut → {status.name}")
                    print(f"[Serveur] Mise a Jour 👾")
                    await self.change_presence(status=discord.Status.idle, activity=status)
                    await asyncio.sleep(5)

        self.loop.create_task(status_cycle())


# Création du bot avec les intents et sans la commande d'aide par défaut
intents = discord.Intents.all()
bot = MonBot(command_prefix='!', intents=intents, help_command=None)

# Suppression de la commande d'aide par défaut
bot.remove_command('help')

@bot.command()
async def help(ctx):
    """Affiche la liste des commandes disponibles"""
    embed = discord.Embed(
        title="Commandes Disponibles",
        description="Voici la liste des commandes que je peux exécuter :",
        color=discord.Color.blue()
    )

    # Liste des commandes et de leurs descriptions
    commands_list = {
        '!help': 'Affiche ce message d\'aide.',
        '/game': 'Vérifie la latence du bot.',
        '/game': 'Lance un jeu de devinette de nombre.',
        # Ajoute ici les autres commandes et leurs descriptions
    }

    for command_name, command_desc in commands_list.items():
        embed.add_field(
            name=f'!{command_name}',
            value=command_desc,
            inline=False
        )

    await ctx.send(embed=embed)

# Garde le bot en ligne
keep_alive()

# Lancer le bot
bot.run(token)
