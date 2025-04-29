import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed

class TicketView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Ouvrir un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Créer un salon pour le ticket
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        
        # Si la catégorie "Tickets" n'existe pas, crée-la
        if not category:
            category = await guild.create_category("Tickets")
        
        # Créer un salon privé pour le ticket
        ticket_channel = await category.create_text_channel(f"ticket-{interaction.user.name}", overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        })
        
        # Envoyer un message de bienvenue dans le salon du ticket
        await ticket_channel.send(f"Ticket ouvert par {interaction.user.mention}. Un membre de l'équipe va vous aider.")

        # Avertir l'utilisateur que le ticket a été ouvert
        await interaction.response.send_message(f"Ticket ouvert dans {ticket_channel.mention}.", ephemeral=True)

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        # Vérifier si l'utilisateur est un administrateur
        if not any(role.name == "Admin" for role in ctx.author.roles):
            await ctx.send("Désolé, vous devez être un administrateur pour utiliser cette commande.")
            return

        # Créer la vue et le bouton
        view = TicketView()

        # Envoyer un message embed avec le bouton
        embed = Embed(
            title="Système de Ticket",
            description="Cliquez sur le bouton ci-dessous pour ouvrir un ticket. Un membre de notre équipe vous assistera.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
