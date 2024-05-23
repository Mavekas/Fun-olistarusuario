import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGODB_TOKEN"))
bancodedados = client["economia"]
usuarios = bancodedados["usuarios"]

async def novo_usuario(usuario):
    filtro = {"discord_id":usuario.id}
    if usuarios.count_documents(filtro) == 0:
        objeto = {
            "discord_id":usuario.id,
            "moedas" : 1000
        }
        usuarios.insert_one(objeto)
        return objeto
    else:
        return False

async def checar_saldo(usuario):
    await novo_usuario(usuario)

    filtro = {"discord_id":usuario.id}
    resultado = usuarios.find(filtro)

    return resultado[0]["moedas"]

async def alterar_saldo(usuario,quantidade):
    await novo_usuario(usuario)

    moedas_atuais=await checar_saldo(usuario)

    filtro = {"discord_id":usuario.id}
    relacao = {"$set": {
        "moedas":moedas_atuais+quantidade
    }}

    usuarios.update_one(filtro,relacao)

async def ranking_usuarios():
    # Ordena os usuários pelo número de moedas em ordem decrescente
    usuarios_ranking = usuarios.find().sort("moedas", pymongo.DESCENDING)

    ranking = []

    for posicao, usuario in enumerate(usuarios_ranking, start=1):
        discord_id = usuario["discord_id"]
        moedas = usuario["moedas"]
        ranking.append({"posicao": posicao, "discord_id": discord_id, "moedas": moedas})

    return ranking
