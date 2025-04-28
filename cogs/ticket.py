import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class TicketView(discord.ui.View):
    def __init__(self, moderator_role: discord.Role, ping_role: discord.Role):
        super().__init__(timeout=None)
        self.moderator_role = moderator_role
        self.ping_role = ping_role

    @discord.ui.button(label="🎟️ Créer un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Vérifie si l'utilisateur a déjà un ticket
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            await interaction.response.send_message(f"🚫 Tu as déjà un ticket ici : {existing_channel.mention}", ephemeral=True)
            return

        # Permissions : user + modérateur
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            self.moderator_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        ticket_channel = await guild.create_text_channel(f"ticket-{user.id}", overwrites=overwrites)

        await ticket_channel.send(f"{self.ping_role.mention} {user.mention} merci d'avoir ouvert un ticket ! Le staff arrivera bientôt.")

        await interaction.response.send_message(f"✅ Ticket créé : {ticket_channel.mention}", ephemeral=True)

        # Ajouter un bouton "Fermer le ticket"
        await ticket_channel.send(view=CloseTicketView())

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fermer le Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Fermeture du ticket dans 5 secondes...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket", description="Configurer le système de tickets")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("Veuillez choisir le salon où envoyer le système de tickets :", ephemeral=True, view=SalonSelector(self.bot))

    @setup_ticket.error
    async def setup_ticket_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("🚫 Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

class SalonSelector(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot

    @discord.ui.select(placeholder="📢 Choisissez un salon", select_type=discord.ComponentType.select, options=[])
    async def select_channel(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Choisir salon + demander rôles
        channel_id = int(select.values[0])
        self.selected_channel = interaction.guild.get_channel(channel_id)

        await interaction.response.send_message(
            "Merci ! Maintenant, mentionne le **rôle modérateur** (ex: @modo) :", ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            moderator_role = msg.role_mentions[0]

            await interaction.followup.send(
                "Super ! Maintenant mentionne le **rôle à ping** lors de l'ouverture d'un ticket :", ephemeral=True
            )

            msg2 = await self.bot.wait_for("message", timeout=60.0, check=check)
            ping_role = msg2.role_mentions[0]

            embed = discord.Embed(
                title="🎫 Ouvre un ticket",
                description="Clique sur le bouton ci-dessous pour créer ton ticket !",
                color=discord.Color.blurple()
            )

            await self.selected_channel.send(embed=embed, view=TicketView(moderator_role, ping_role))
            await interaction.followup.send("✅ Système de tickets configuré avec succès !", ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.followup.send("⏳ Temps écoulé. Merci de relancer la commande.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
