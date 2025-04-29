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

        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            await interaction.response.send_message(f"🚫 Tu as déjà un ticket ici : {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            self.moderator_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        ticket_channel = await guild.create_text_channel(f"ticket-{user.id}", overwrites=overwrites)

        await ticket_channel.send(f"{self.ping_role.mention} {user.mention} merci d'avoir ouvert un ticket ! Le staff arrivera bientôt.")
        await interaction.response.send_message(f"✅ Ticket créé : {ticket_channel.mention}", ephemeral=True)
        await ticket_channel.send(view=CloseTicketView())

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fermer le Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Fermeture du ticket dans 5 secondes...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class SalonSelector(discord.ui.View):
    def __init__(self, bot, interaction_user):
        super().__init__(timeout=60)
        self.bot = bot
        self.interaction_user = interaction_user

        options = []
        for channel in bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                options.append(
                    discord.SelectOption(
                        label=channel.name,
                        value=str(channel.id),
                        description="Salon texte"
                    )
                )

        select = discord.ui.Select(
            placeholder="📢 Choisissez un salon",
            options=options,
            min_values=1,
            max_values=1
        )
        select.callback = self.select_channel
        self.add_item(select)

    async def select_channel(self, interaction: discord.Interaction):
        if interaction.user != self.interaction_user:
            await interaction.response.send_message("🚫 Seul l'utilisateur ayant lancé la commande peut faire ça.", ephemeral=True)
            return

        selected_channel_id = int(interaction.data["values"][0])
        selected_channel = interaction.guild.get_channel(selected_channel_id)

        await interaction.response.send_message("Mentionne maintenant le **rôle modérateur** (ex: @modérateur) :", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

        try:
            msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            moderator_role = msg.role_mentions[0]

            await interaction.followup.send("Et maintenant, mentionne le **rôle à ping** quand un ticket s'ouvre :", ephemeral=True)
            msg2 = await self.bot.wait_for("message", timeout=60.0, check=check)
            ping_role = msg2.role_mentions[0]

            embed = discord.Embed(
                title="🎫 Ouvre un ticket",
                description="Clique sur le bouton ci-dessous pour créer ton ticket !",
                color=discord.Color.blurple()
            )

            await selected_channel.send(embed=embed, view=TicketView(moderator_role, ping_role))
            await interaction.followup.send("✅ Système de tickets configuré avec succès !", ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.followup.send("⏳ Temps écoulé. Merci de relancer la commande.", ephemeral=True)

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket", description="Configurer le système de tickets")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("📢 Choisissez un salon pour configurer le système de tickets :", ephemeral=True)
        await interaction.channel.send(view=SalonSelector(self.bot, interaction.user))

    @setup_ticket.error
    async def setup_ticket_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("🚫 Tu n'as pas la permission d’utiliser cette commande.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
