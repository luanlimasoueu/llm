import streamlit as st
import rag_backend as demo


if 'vector_index' not in st.session_state:
    with st.spinner("Hora da mágica"):
        st.session_state.vector_index = demo.hr_index()

input_text = st.text_area("Input", label_visibility="collapsed")
go_button = st.button("Learn", type="primary")

if go_button:

    with st.spinner(" Esperando"):
        response_content = demo.hr_rag_response(index= st.session_state.vector_index, question=input_text)
        st.write(response_content)


