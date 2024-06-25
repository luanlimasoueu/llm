import streamlit as st

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.message = []

#Display chat messages from history on app rerun
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.message.append({"role":"user", "content": prompt})

    response = f"Echo: {prompt}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.message.append({"role":"assistant", "content": response})
    