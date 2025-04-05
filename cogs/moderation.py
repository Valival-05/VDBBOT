import discord
from discord.ext import commands
from discord import app_commands

class ModerationView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger)
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Tu n'as pas la permission pour faire ça.", ephemeral=True)
            return

        await self.member.kick(reason=f"Kicked by {interaction.user}")
        await interaction.response.edit_message(content=f"{self.member} a été kické !", view=None)

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.danger)
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Tu n'as pas la permission pour faire ça.", ephemeral=True)
            return

        await self.member.ban(reason=f"Banned by {interaction.user}")
        await interaction.response.edit_message(content=f"{self.member} a été banni !", view=None)

    @discord.ui.button(label="Mute", style=discord.ButtonStyle.secondary)
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("La fonction mute n'est pas encore implémentée.", ephemeral=True)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.grey)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Action annulée.", view=None)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="moderate", description="Afficher les options de modération pour un membre.")
    @app_commands.checks.has_permissions(administrator=True)
    async def moderate(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(
            title="Options de modération",
            description=f"Que veux-tu faire avec {member.mention} ?",
            color=discord.Color.red()
        )
        view = ModerationView(member)
        await interaction.response.send_message(embed=embed, view=view)

    @moderate.error
    async def moderate_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Tu dois être administrateur pour utiliser cette commande.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
