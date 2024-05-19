import os
import boto3
import json
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConstitutionalChain



#def demo_chatbot():

import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()
# Acessando a variável de ambiente API_KEY

boto3.setup_default_session(aws_access_key_id = os.getenv("aws_access_key_id"),
                            aws_secret_access_key= os.getenv("aws_secret_access_key"),
                            region_name = os.getenv("region_name"))
bedrock = boto3.client(service_name="bedrock-runtime")

bedrock = boto3.client(service_name="bedrock-runtime")

prompt = "Camberra is capital of Australia"

body = json.dumps({
    "inputText": prompt
})

model_id = 'amazon.titan-embed-text-v1'
accept = 'application/json'
content_type = 'application/json'

response = bedrock.invoke_model(
    body = body,
    modelId = model_id,
    accept = accept,
    contentType = content_type
)

response_body = json.loads(response['body'].read())
embedding = response_body.get('embedding')
print(embedding)
