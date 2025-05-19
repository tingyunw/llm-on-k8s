import requests
import streamlit as st
from loguru import logger
import os
import sys
from config.ap_config import router_url


def on_click():
    st.session_state.user_input = ""


def send_request(user_input):
    path_params = dict()
    path_params["question"] = user_input

    with requests.post(f"{router_url}/ask_llm_and_get_response", data=path_params) as response:
        if response.status_code == 200:
            return response.json()["response"]
        else:
            logger.error("Failed:", response.status_code, response.text)
            return "500 Internal Server Error"


def main():
    st.title("Ask a question to DeepSeek-R1")

    # Input text box
    user_input = st.text_input("Enter your question:", key="user_input")

    # Display output fields
    if user_input:
        st.write("### Output:")
        st.write(f"You question: {user_input}")
        st.write(f"Answer from DeepSeek-R1: {send_request(user_input)}")
        st.button("Clear", on_click=on_click)


if __name__ == "__main__":
    main()
