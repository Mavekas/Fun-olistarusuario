import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGODB_TOKEN"))
bancodedados = client["economia"]
usuarios = bancodedados["usuarios"]

async def novo_usuario(usuario):
    filtro = {"discord_id": usuario.id}
    if usuarios.count_documents(filtro) == 0:
        objeto = {
            "discord_id": usuario.id,
            "moedas": 1000
        }
        usuarios.insert_one(objeto)
        return objeto
    else:
        return False

async def checar_saldo(usuario):
    await novo_usuario(usuario)

    filtro = {"discord_id": usuario.id}
    resultado = usuarios.find(filtro)

    return resultado.__getitem__(0)["moedas"]

async def alterar_saldo(usuario, quantidade):
    await novo_usuario(usuario)

    moedas_atuais = await checar_saldo(usuario)

    filtro = {"discord_id": usuario.id}
    relacao = {"$set": {
        "moedas": moedas_atuais + quantidade
    }}

    usuarios.update_one(filtro, relacao)

async def remover_usuario(usuario):
    filtro = {"discord_id": usuario.id}
    resultado = usuarios.delete_one(filtro)
    if resultado.deleted_count > 0:
        return True
    else:
        return False
