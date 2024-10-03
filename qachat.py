from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API with the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Error: API key not found in environment variables.")
    st.stop()

genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
def get_gemini_response(question):
    """Fetches response from Gemini Pro model for a given question."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"An error occurred while fetching the response: {e}")
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="centered")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input section
user_input = st.text_input("Ask a question:", key="input")

if st.button("Submit") and user_input:
    response = get_gemini_response(user_input)

    if response:
        # Add user query to chat history
        st.session_state['chat_history'].append(("You", user_input))
        st.subheader("Response:")
        
        # Stream the response in chunks
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
if st.session_state['chat_history']:
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.markdown(f"**{role}:** {text}")
