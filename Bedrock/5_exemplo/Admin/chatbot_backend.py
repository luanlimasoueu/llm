import os
import boto3
import json
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConstitutionalChain

import base64
from io import BytesIO
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

boto3.setup_default_session(
aws_access_key_id = os.getenv("aws_access_key_id"),
aws_secret_access_key= os.getenv("aws_secret_access_key"),
    region_name = os.getenv("region_name"),
)
                            


# AWS Bedrock client setup for stable diffusion model
aws_bedrock = boto3.client('bedrock-runtime')
bedrock_model_id = "stability.stable-diffusion-xl-v1"

def decode_image_from_response(response):
    """
    Decodes the image from the model's response.
    """
    response_body = json.loads(response['body'].read())
    image_artifacts = response_body['artifacts']
    image_bytes = base64.b64decode(image_artifacts[0]['base64'])
    return BytesIO(image_bytes)

def generate_image(prompt, style):
    """
    Generates an image based on the provided prompt and style.
    """
    
    request_payload = json.dumps({
        "text_prompts": [{"text": f"{style} {prompt}"}],
        "cfg_scale":9, #default fidelity to prompt
        "steps": 50, # default detail level
    })
    
    model_response = aws_bedrock.invoke_model(body = request_payload, modelId = bedrock_model_id)
    return decode_image_from_response(model_response)

# Streamlit interface setup with custom styles
st.set_page_config(page_title="Personalized Artwork Creator", layout="wide")

#set background to black and adjust text colors for visibility
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000; /* Black background */
    }
    h1, h2, h3, h4, h5, h6, .stTextArea, .stTextInput, .stMarkdown, body, .st-bb, .st-at, .st-cb, .st-dg, .st-dh, .st-di, .st-ea, .st-eb, .stSelectbox > div > div > ul > li {
        color: #FFFFFF; /* White font color for better visibility */
    }
    .stButton > button {
        color: #FFFFFF; /* White font color for button text */
        border-color: #FFFFFF; /* White border for buttons */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Personalized Artwork Creator")
prompt_column, result_column = st.columns(2)

with prompt_column:
    st.subheader("Customize your artwork")
    prompt_text = st.text_area("Describe the scene", height = 150)
    art_style = st.selectbox("Choose a style", ["Abstract", "Cute", "Fantasy", "Futuristic", "Realistic", "Science Fiction", "Surreal", "Techno"])
    generate_button = st.button("Generate Artwork")
    
with result_column:
    st.subheader("Your Generated Artwork")
    if generate_button:
        with st.spinner("Creating Artwork...."):
            artwork_image = generate_image(prompt_text, art_style)
        st.image(artwork_image, use_column_width=True)