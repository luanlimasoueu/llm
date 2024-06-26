import os
import boto3
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import Bedrock

boto3.setup_default_session(
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key"),
     region_name="us-east-1"
)
                            
bedrock_runtime = boto3.client(service_name='bedrock-runtime')


def hr_index():
        data_load = PyPDFLoader('jogo.pdf')
        data_split = RecursiveCharacterTextSplitter(chunk_size= 200,chunk_overlap=200 )


        
        
        bedrock_embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1", 
            credentials_profile_name= "default"
        )


        data_index = VectorstoreIndexCreator(
            text_splitter=data_split,
            embedding=bedrock_embeddings,
            vectorstore_cls= FAISS
        )

        db_index = data_index.from_loaders( [data_load])
        return  db_index


def hr_llm():
        llm = Bedrock(
        credentials_profile_name="default", 
        model_id="anthropic.claude-v2",
        model_kwargs={"temperature": 1, "top_p": 0.9, "max_tokens_to_sample": 3000}
        )
        return llm

def hr_rag_response(index, question):
        rag_llm = hr_llm()
        hr_rag_query = index.query(question=question, llm=rag_llm)
        return hr_rag_query