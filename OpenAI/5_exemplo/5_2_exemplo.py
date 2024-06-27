import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key


modelo = OpenAI(api_key=api_key)
                                      
resposta = modelo('What are the two guidelines?')
print(resposta)
