# from talk_to_docs_pdf_txt_from_dir import ask_ai_st
import streamlit as st
from streamlit_extras.app_logo import add_logo
import streamlit_image_coordinates
from PIL import Image

import os
from dotenv import load_dotenv, find_dotenv

import openai
from llama_index import load_index_from_storage, StorageContext

 # Read local .env file to acquire necessary API keys
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_ai_st(query):
    """Langchain + OpenAI"""
    # index = GPTVectorStoreIndex.load_from_disk('index.json')
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # load index
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    print("Asking loop starting ...")
    
    template = f" Use the information that has been provided through the document you're trained on to answer the following question: {query}"
        
    response = query_engine.query(template)

    return response


def main():
    #print("In main ...")
    st.set_page_config(page_title="Chat with Measurements Manual", page_icon=":books")

    # Create a storage
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.subheader(":chart_with_downwards_trend: :rainbow[Ask Measurements and Evaluation System Manual] :chart_with_upwards_trend:")
    # st.header(":bar_chart: :rainbow[إسأل دليل القياس التابع لجامعة عين شمس] :page_with_curl: :page_with_curl: :pushpin:")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message.get("role")):
            st.markdown(message.get("content"))

    prompt  = st.chat_input("Ask something...")

    if prompt:
        # Added to storage
        st.session_state.messages.append({"role": "user", "content":prompt})
        # Display whay was typed
        with st.chat_message("user"):
            st.write(prompt)

        # process with LLM or NLP
        response = "respond" # ask_ai_st(prompt)

        # Store response
        st.session_state.messages.append({"role":"assistant", "content":response})

        with st.chat_message("assistant"):
            st.markdown(response)


    # Sidebar to the 
    with st.sidebar:        
        # Titles
        # # Define custom HTML element for Arabic title
        # html_title_ar = """
        # <div style="text-align: center; padding: 10px 0;">
        # <h1 style="color: #ff3900; font-weight: bold; text-align: center;">
        # دليل منظومة القياس والتقويم بجامعة عين شمس
        # </h1>
        # </div>
        # """
        # st.markdown(html_title_ar, unsafe_allow_html=True)

        # # Define custom HTML element for English title
        # html_string = """
        # <div style="text-align: center; padding: 5px 0;">
        # <h2 style="color: #00008b; font-weight: bold; text-align: center;">
        # Guide to the measurement and evaluation system at Ain Shams University
        # </h2>
        # </div>
        # """
        
        # st.header("Guide to the measurement and evaluation system at Ain Shams University")
        # st.header("دليل منظومة القياس والتقويم بجامعة عين شمس")

        image_01 = Image.open("media/banner-1-removebg.png")
        st.image(image_01, use_column_width=True)

        options = ["English", "Arabic"]
        st.subheader(":blue[Choose conversation langugage: ]")
        # st.subheader(":green['اختر لغة للحوار مع الدليل']")
        selected_option = st.selectbox("", options=options, index=1)

        # if st.button("Process"):
        #     with st.spinner("processing..."):
        #         # get pdf text
        #         st.write("You selected:", selected_option)

        #         # get the text chunks


if __name__ == '__main__':
    #print("starting ...")
    main()
    # ask_ai()