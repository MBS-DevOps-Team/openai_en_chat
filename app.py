# from talk_to_docs_pdf_txt_from_dir import ask_ai_st
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

import openai
from llama_index import load_index_from_storage, StorageContext

 # Read local .env file to acquire necessary API keys
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_ai_st(query):
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
    print("In main ...")
    # Create a storage
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    print("History: \n\n")
    for message in st.session_state.messages:
        with st.chat_message(message.get("role")):
            print("Role: ", message.get("role"))
            print("Content: ", message.get("content"), "\n\n")
            st.markdown(message.get("content"))

    print("End History. \n\n")

    prompt  = st.chat_input("Ask something...")

    if prompt:
        print("Prompt started...")
        # Added to storage
        st.session_state.messages.append({"role": "user", "content":prompt})
        # Display whay was typed
        with st.chat_message("user"):
            st.write(prompt)

        # process with LLM or NLP
        response = ask_ai_st(prompt)

        # Store response
        st.session_state.messages.append({"role":"assistant", "content":response})

        with st.chat_message("assistant"):
            st.markdown(response)
            print("Response: ", response)

if __name__ == '__main__':
    print("starting ...")
    main()
    # ask_ai()