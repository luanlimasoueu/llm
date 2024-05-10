import streamlit as st 
import pickle
import os
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

with st.sidebar:
    st.title("LLM Chat App")

    add_vertical_space (5)
    st.write("Luan Lima")

def main():
    st.write("Hello")
    
    os.environ['OPENAI_API_KEY'] = ''


    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        
        text = " "
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )

        chunks = text_splitter.split_text(text = text)

        store_name = pdf.name[:-4]

        if os.path.exists (f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write('Embeddings Loaded from the Disk')
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts (chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                 pickle.dump(VectorStore, f)
            st.write('Embeddings Computation Completed')

if __name__ == '__main__':
    main()