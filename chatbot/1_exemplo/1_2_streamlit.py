import streamlit as st


st.title("Echo Bot")

if "messages" not in st.session_state:
    st.session_state.message = []

#Display chat messages from history on app rerun
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#React to user input
prompt = st.chat_input("What is up?")
if prompt:
    #Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    #Add user message to chet history
    st.session_state.message.append({"role":"user", "content": prompt})

    response = f"Echo: {prompt}"
    
    #Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    #Add assistant response chat history
    st.session_state.message.append({"role":"assistant", "content": response})
    