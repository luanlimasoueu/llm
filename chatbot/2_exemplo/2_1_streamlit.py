import streamlit as st
import openai
import os

st.title("Echo Bot")

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Streamlit UI
st.title("Vitamin Quiz Bot")

# Initialize session state
if 'iteration' not in st.session_state:
    st.session_state.iteration = 0
    st.session_state.quiz_active = False

# Main loop for the quiz
user_input = st.text_input("You (Iteration {}):".format(st.session_state.iteration))

if user_input.lower() == "lets begin the quiz":
    st.session_state.quiz_active = True

if st.session_state.quiz_active:
    # Generate a question
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate a question about vitamins and minerals for a 3rd-grade quiz."},
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        max_tokens=50,
        temperature=0.7,
    )
    question = response.choices[0].message.content.strip()

    # Display the question
    st.text("Bot: {}".format(question))

    # Get user's response
    user_response = st.text_input("You:")

    # Evaluate the response
    if st.button("Submit"):
        st.text("You said: {}".format(user_response))