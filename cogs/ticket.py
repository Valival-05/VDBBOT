import discord
import asyncio
from discord.ext import commands
from discord import app_commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Ouvrir un Ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Vérifie si l'utilisateur a déjà un ticket
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            await interaction.response.send_message(f"🚫 Tu as déjà un ticket ici : {existing_channel.mention}", ephemeral=True)
            return

        # Cherche une catégorie spécifique (optionnel)
        category = discord.utils.get(guild.categories, name="🎫 Tickets")
        if category is None:
            # Si la catégorie n'existe pas, elle est créée automatiquement
            category = await guild.create_category("🎫 Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket ouvert par {user.name} ({user.id})"
        )

        # Message dans le ticket avec un bouton pour fermer
        embed = discord.Embed(
            title="🎟️ Ticket Ouvert",
            description="Merci d'avoir ouvert un ticket ! Le staff va te répondre sous peu.\n\nPour fermer ce ticket, utilise le bouton ci-dessous 👇",
            color=discord.Color.green()
        )
        await ticket_channel.send(content=f"{user.mention}", embed=embed, view=CloseTicketView())

        await interaction.response.send_message(f"✅ Ton ticket a été créé : {ticket_channel.mention}", ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fermer le Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel

        # Confirmation de fermeture
        embed = discord.Embed(
            title="Confirmation",
            description="⏳ Fermeture du ticket dans 5 secondes...",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(5)
        await channel.delete()

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket", description="Configurer le système de tickets avec bouton")
    async def setup_ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Besoin d'aide ?",
            description="Clique sur le bouton ci-dessous pour ouvrir un ticket avec le staff.",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
