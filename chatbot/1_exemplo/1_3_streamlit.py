import streamlit as st
import openai
import os

st.title("Echo Bot")

openai.api_key = os.environ.get("OPENAI_API_KEY")
# Initialize chat history

if "openai_model" not in st.session_state:
     st.session_state["openai_model"] = "gpt-3.5-turbo"
     
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#React to user input
prompt = st.chat_input("What is up?")
if prompt:
    #Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    #Add user message to chet history
    st.session_state.messages.append({"role":"user", "content": prompt})

    
    #Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.chat.completions.create(

            model = st.session_state["openai_model"],

            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True

        ):
            #response.choices[0].delta.get("content", "")
            pedaco_da_resposta= response.choices[0].delta.content

            if pedaco_da_resposta is None:
                pedaco_da_resposta = ""

            full_response +=  pedaco_da_resposta
            message_placeholder.markdown(full_response + " ")
        
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({ "role": "assistant", "content": full_response})