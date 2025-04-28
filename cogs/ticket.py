import discord
from discord.ext import commands
from discord import app_commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Créer un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Vérifie si l'utilisateur a déjà un ticket
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            await interaction.response.send_message(f"🚫 Tu as déjà un ticket ici : {existing_channel.mention}", ephemeral=True)
            return

        # Création du salon
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticket_channel = await guild.create_text_channel(f"ticket-{user.id}", overwrites=overwrites)
        await ticket_channel.send(f"{user.mention} merci d'avoir ouvert un ticket ! Le staff va arriver.")

        await interaction.response.send_message(f"✅ Ticket créé : {ticket_channel.mention}", ephemeral=True)

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket", description="Configurer le système de tickets")
    async def setup_ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Système de Tickets",
            description="Clique sur le bouton ci-dessous pour ouvrir un ticket.",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
