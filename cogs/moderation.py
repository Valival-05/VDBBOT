# cogs/moderation.py
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        await ctx.send(f'{member} has been kicked!')

async def setup(bot):
    await bot.add_cog(Moderation(bot))  # Assurez-vous que 'add_cog' est correctement 'awaité'
