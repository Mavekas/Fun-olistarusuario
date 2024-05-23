import pymongo
from dotenv import load_dotenv
import os
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Configuração do cliente MongoDB
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

# Função para listar todos os usuários
async def listar_usuarios():
    try:
        usuarios_lista = await usuarios.find().to_list(length=None)
        return [{"discord_id": u["discord_id"], "moedas": u["moedas"]} for u in usuarios_lista]
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        return []
