from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain_community.document_loaders import TextLoader


loader = TextLoader('state_of_the_union.txt',  encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(texts, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)

query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)

