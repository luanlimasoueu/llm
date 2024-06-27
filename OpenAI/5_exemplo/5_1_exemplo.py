
import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

template = PromptTemplate.from_template("Responda a seguinte pergunta: {pergunta}")
modelo = OpenAI(api_key=api_key)
                                      
prompt = template.format(pergunta="O que é um buraco negro?")
print(prompt)

resposta = modelo.invoke(prompt)
print(resposta)
