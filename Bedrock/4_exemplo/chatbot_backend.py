import boto3
import json
import os
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import  ConversationChain


from dotenv import load_dotenv



load_dotenv()

def demo_chatbot():
    
    boto3.setup_default_session(
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key"),
    region_name = os.getenv("region_name"),
    )
                            
    bedrock_runtime = boto3.client(service_name='bedrock-runtime')


    demo_llm = Bedrock(
    model_id='meta.llama2-70b-chat-v1',
    client=bedrock_runtime,
    model_kwargs={
        "temperature": 0.9,
        "top_p": 0.5,
        "max_gen_len": 512
    })

    return  demo_llm

def demo_memory():
    llm_data = demo_chatbot()
    memory = ConversationBufferMemory(
        llm = llm_data,
        max_token_limit = 512
    )
    return memory

def demo_conversation (input_text, memory):
    llm_chain_data = demo_chatbot()
    llm_conversation = ConversationChain(llm=llm_chain_data, memory=memory, verbose=True)

    chat_reply = llm_conversation.predict(input=input_text)
    return chat_reply