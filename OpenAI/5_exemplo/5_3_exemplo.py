import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

doc_loader = TextLoader('article.txt')
documents = doc_loader.load()


text_splitter = CharacterTextSplitter(chunk_overlap=0, chunk_size=1000)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
docsearch = Chroma.from_documents(texts, embeddings)

modelo = OpenAI(api_key=api_key)

resposta = modelo.invoke(docsearch)
print(resposta)
