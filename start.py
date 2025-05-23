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
        print(f'✅ Bot connecté en tant que {self.user}')

        # Synchronisation manuelle à chaque démarrage
        await self.tree.sync()
        commands_synced = await self.tree.fetch_commands()
        print(f"✅ Slash commands synchronisées ({len(commands_synced)} commandes)")
        
        # --- Envoi de messages dans plusieurs canaux ---
        channel_ids = [
            1353147720864501764,  # ID canal 1
            1364669476544712791,  # ID canal 2
            1355857690852724837   # ID canal 3
        ]

        for channel_id in channel_ids:
            try:
                channel = await self.fetch_channel(channel_id)
                await channel.send("🎉 Le bot est en ligne et prêt à l’action !")
                await asyncio.sleep(1)
                await channel.send("⏳ Initialisation en cours...")
                await asyncio.sleep(3)
                await channel.send("✅ Tous les systèmes sont opérationnels.")
                await asyncio.sleep(7)
                await channel.send("❌ Non ce message n'est pas généré par IA")
            except Exception as e:
                print(f"[ERREUR] Envoi échoué dans le salon {channel_id} : {e}")

        # --- Rotation des statuts ---
        statuses = [
            discord.Game("Dev"),
            discord.Activity(type=discord.ActivityType.watching, name="la description du BOT"),
            discord.Activity(type=discord.ActivityType.watching, name="Le discord Officiel"),
            discord.Activity(type=discord.ActivityType.listening, name="de la musique")
        ]

        async def status_cycle():
            while True:
                for status in statuses:
                    print(f"[DEBUG] Changement de statut → {status.name}")
                    await self.change_presence(status=discord.Status.idle, activity=status)
                    await asyncio.sleep(10)

        self.loop.create_task(status_cycle())

# Création du bot avec les intents et sans la commande d'aide par défaut
intents = discord.Intents.all()
bot = MonBot(command_prefix='/', intents=intents, help_command=None)

# Suppression de la commande d'aide par défaut
bot.remove_command('help')

@bot.command()
async def help(ctx):
    """Affiche la liste des commandes disponibles"""
    embed = discord.Embed(
        title="Commandes Disponibles",
        description="Voici la liste des commandes que je peux exécuter (En développement ⚠️ ...):",
        color=discord.Color.blue()
    )

    # Liste des commandes et de leurs descriptions
    commands_list = {
        'help': 'Affiche ce message d\'aide.',
        'game': 'Lance un jeu de devinette de nombre.',
        'Setup_ticket': 'Permet de setup le système de ticket. En développement ⚠️',
    }

    for command_name, command_desc in commands_list.items():
        embed.add_field(
            name=f'/{command_name}',
            value=command_desc,
            inline=False
        )

    await ctx.send(embed=embed)

# Garde le bot en ligne
keep_alive()

# Lancer le bot
bot.run(token)
