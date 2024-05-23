import discord
from dotenv import load_dotenv
from discord import app_commands
import os

from database import novo_usuario, checar_saldo, alterar_saldo, remover_usuario

load_dotenv()


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(name='saldo', description='Veja o seu saldo no bot')
async def saldo(interaction: discord.Interaction):
    moedas = await checar_saldo(interaction.user)
    await interaction.response.send_message(f"Você tem {moedas} moedas")

@tree.command(name="daily", description="Ganhe moedas")
async def daily(interaction: discord.Interaction):
    await alterar_saldo(interaction.user, 500)
    await interaction.response.send_message(f"{interaction.user.mention} ganhou 500 moedas")

@tree.command(name='pagamento', description='Pague a um usuario no discord')
async def pagamento(interaction: discord.Interaction, usuario: discord.User, valor: int):
    moedas = await checar_saldo(interaction.user)
    if moedas >= valor:
        await alterar_saldo(interaction.user, -valor)
        await alterar_saldo(usuario, valor)
        await interaction.response.send_message(f"O valor foi enviado com sucesso")
    else:
        await interaction.response.send_message(f"Você não tem saldo")

@tree.command(name='remover', description='Remove um usuario do banco de dados')
async def remover(interaction: discord.Interaction, usuario: discord.User):
    resultado = await remover_usuario(usuario)
    if resultado:
        await interaction.response.send_message(f"O usuário {usuario.mention} foi removido com sucesso.")
    else:
        await interaction.response.send_message(f"O usuário {usuario.mention} não foi encontrado no banco de dados.")


aclient.run(os.getenv("BOT_TOKEN"))
