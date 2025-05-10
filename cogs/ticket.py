import discord
from discord.ext import commands
from discord import app_commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Ouvrir un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True),
        }

        # Vérifie si un ticket existe déjà
        for channel in guild.text_channels:
            if channel.name == f"ticket-{user.name.lower()}":
                await interaction.response.send_message("❗ Tu as déjà un ticket ouvert.", ephemeral=True)
                return

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites,
            topic=f"Ticket de {user.name}",
            reason="Ouverture de ticket"
        )

        await ticket_channel.send(f"{user.mention} merci pour ton ticket. Un membre du staff te répondra bientôt.")
        await interaction.response.send_message(f"✅ Ticket créé : {ticket_channel.mention}", ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket", description="Configurer le système de ticket")
    @commands.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction):
        view = TicketView()
        await interaction.response.send_message("Clique sur le bouton ci-dessous pour ouvrir un ticket :", view=view)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
