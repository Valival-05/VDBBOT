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
        await interaction.response.send_message("🔇 Mute non implémenté pour le moment.", ephemeral=True)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.grey)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Action annulée.", view=None)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Commande slash /moderate
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
            await interaction.response.send_message("❌ Tu dois être administrateur pour utiliser cette commande.", ephemeral=True)

    # ✅ Commande !sync (admin only) – synchro instantanée sur le serveur actuel
    @commands.command(name="sync")
    @commands.has_permissions(administrator=True)
    async def sync_commands(self, ctx):
        synced = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Commandes slash synchronisées pour **{ctx.guild.name}** : {len(synced)} commandes.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
