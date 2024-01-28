import streamlit as st
from responses import reply
import asyncio
from PIL import Image

st.set_page_config(page_title="APU Live Chatbot", page_icon="images/bot_pic.png")
st.title("APU Knowledge Live Assistant")
    
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I am APU Virtual Bot. You may ask me anything about the facilities and services in APU."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="images/bot_pic.png" if message["role"] == "assistant" else None):
        st.markdown(message["content"], unsafe_allow_html=True)

if user_input := st.chat_input(placeholder="Ask anything about APU"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar="images/bot_pic.png"):
        with st.spinner("Thinking..."):
            response = str(asyncio.run(reply(user_input))).strip().replace("\n", "<br>")
            st.markdown(response, unsafe_allow_html=True) 
            if "hi" == user_input:
                bot_image = Image.open("images/hi.gif")
                st.image(bot_image, caption="hi", use_column_width=True)
            if "parking rate" in response.lower():
                bot_image = Image.open("images/apu_map.jpeg")
                st.image(bot_image, caption="APU Map", use_column_width=True)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)