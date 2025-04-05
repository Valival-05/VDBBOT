# cogs/games.py
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello from the Games cog!")

# Cette fonction 'setup' est ce qui permet au bot de charger la cog correctement.
async def setup(bot):
    await bot.add_cog(Games(bot))  # Assurez-vous que cette ligne utilise await correctement
