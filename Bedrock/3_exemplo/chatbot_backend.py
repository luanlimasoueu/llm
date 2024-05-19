import os
import boto3
import json
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConstitutionalChain



#def demo_chatbot():

import os
from dotenv import load_dotenv

load_dotenv()

def demo_chatbot(input_text):
    demo_llm = Bedrock(
    model_id='meta.llama2-70b-chat-v1',
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key"),
    region_name = os.getenv("region_name"),
    model_kwargs={
        "temperature": 0.9,
        "top_p": 0.5,
        "max_gen_len": 512
    })
    return  demo_llm.predict(input_text)
response = demo_chatbot("Hi, what is yor name?")
print(response)