import discord
from discord.ext import commands
import random
import asyncio

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='game', description="Un jeu où tu dois deviner un nombre entre 1 et 100")
    async def guess_number(self, interaction: discord.Interaction):
        """Un jeu où le joueur doit deviner un nombre entre 1 et 100"""
        number_to_guess = random.randint(1, 100)
        attempts = 0
        max_attempts = 5
        
        # Envoie un message pour commencer le jeu
        await interaction.response.send_message(f"Je pense à un nombre entre 1 et 100. Tu as {max_attempts} tentatives pour deviner le bon nombre !")

        # Fonction pour gérer les réponses de l'utilisateur
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        while attempts < max_attempts:
            try:
                # Attends la réponse de l'utilisateur
                response = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess = int(response.content)  # On essaie de convertir la réponse en nombre
                attempts += 1

                if guess < number_to_guess:
                    await interaction.channel.send("C'est plus grand ! Essaie encore.")
                elif guess > number_to_guess:
                    await interaction.channel.send("C'est plus petit ! Essaie encore.")
                else:
                    await interaction.channel.send(f"Bravo ! Tu as deviné le bon nombre {number_to_guess} en {attempts} tentatives.")
                    return

            except ValueError:
                await interaction.channel.send("Ce n'est pas un nombre valide. Essaie encore.")
            except asyncio.TimeoutError:
                await interaction.channel.send(f"Tu as mis trop de temps ! Le nombre était {number_to_guess}.")
                return
        
        await interaction.channel.send(f"Tu as épuisé toutes tes tentatives. Le nombre était {number_to_guess}.")

# Fonction setup pour charger le Cog
async def setup(bot):
    await bot.add_cog(Games(bot))
