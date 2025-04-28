import discord
from discord.ext import commands
from discord import app_commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Pas de timeout pour la View

    @discord.ui.button(label="Créer un ticket 🎫", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Vérifie si l'utilisateur a déjà un ticket ouvert
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"Tu as déjà un ticket ouvert: {existing_channel.mention}", ephemeral=True)
            return

        # Crée un salon privé
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}".lower(),
            overwrites=overwrites,
            reason=f"Ticket créé par {user}."
        )

        await channel.send(f"{user.mention} Bienvenue dans ton ticket. Un membre du staff va bientôt te répondre.")
        await interaction.response.send_message(f"Ton ticket a été créé : {channel.mention}", ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup_ticket")
    @commands.has_permissions(administrator=True)
    async def setup_ticket(self, ctx):
        """Commande pour envoyer le message de création de tickets"""
        embed = discord.Embed(
            title="Support Ticket",
            description="Clique sur le bouton ci-dessous pour créer un ticket 🎟️",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Ticket(bot))
