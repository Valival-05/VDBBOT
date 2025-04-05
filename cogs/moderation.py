import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class ModerationView(discord.ui.View):
    def __init__(self, member: discord.Member, bot):
        super().__init__(timeout=60)
        self.member = member
        self.bot = bot

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
        muted_role = discord.utils.get(self.member.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await self.create_muted_role(self.member.guild)

        await self.member.add_roles(muted_role)
        await interaction.response.edit_message(content=f"{self.member} a été mute !", view=None)

    @discord.ui.button(label="TempMute", style=discord.ButtonStyle.secondary)
    async def tempmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        muted_role = discord.utils.get(self.member.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await self.create_muted_role(self.member.guild)

        await self.member.add_roles(muted_role)
        await interaction.response.edit_message(content=f"{self.member} a été mute pour 10 minutes !", view=None)

        # Temporarily mute for 10 minutes
        await asyncio.sleep(600)  # 10 minutes
        await self.member.remove_roles(muted_role)
        await self.member.send(f"Ton mute temporaire a expiré. Tu es maintenant démuté.")

    @discord.ui.button(label="Unmute", style=discord.ButtonStyle.success)
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        muted_role = discord.utils.get(self.member.guild.roles, name="Muted")
        if muted_role:
            await self.member.remove_roles(muted_role)
            await interaction.response.edit_message(content=f"{self.member} a été unmute !", view=None)
        else:
            await interaction.response.send_message("Ce membre n'est pas mute.", ephemeral=True)

    @discord.ui.button(label="Warn", style=discord.ButtonStyle.blurple)
    async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{self.member} a été averti !", ephemeral=True)
        # You could add logic here for storing warnings, logging, etc.

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.grey)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Action annulée.", view=None)

    async def create_muted_role(self, guild):
        muted_role = await guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
        for channel in guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)
        return muted_role

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
        view = ModerationView(member, self.bot)
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
