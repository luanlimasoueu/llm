import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()
# Acessando a variável de ambiente API_KEY
api_key = os.getenv("API_KEY")
# Verificando se a API_KEY foi carregada com sucesso
if api_key:
    print("Chave de API carregada com sucesso:", api_key)
else:
    print("Chave de API não encontrada no arquivo .env.")