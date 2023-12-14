from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTVectorStoreIndex, LLMPredictor, PromptHelper, ServiceContext, StorageContext, load_index_from_storage
from langchain.llms import OpenAI
import openai
import sys
import os
from dotenv import load_dotenv, find_dotenv
from IPython.display import Markdown, display
import warnings
warnings.filterwarnings("ignore")

 # Read local .env file to acquire necessary API keys
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 10000
    # set maximum chunk overlap
    max_chunk_overlap = 0.2  # = 20
    # set chunk size limit
    chunk_size_limit = 1000 

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    
    # Use Langchain to understand Arabic Text, 
    # Then use the new Text Adaptation at the LLma --> 
    # "text-davinci-300" will not be appropriate --> Look for an adaptaion
    
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.0, model_name="text-davinci-003", max_tokens=num_outputs))
 
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    # index.save_to_disk('index.json')
    index.storage_context.persist()

    return index

def ask_ai():
    # index = GPTVectorStoreIndex.load_from_disk('index.json')
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # load index
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    print("Asking loop starting ...")
    while True: 
        query = input("Ask (quit for exit): ")
        if query == "quit":
            break
        template = f" Use the information that has been provided through the document you're trained on to answer the following question: {query}"
        response = query_engine.query(template)
        # display(Markdown(f"Response: <b>{response.response}</b>"))
        print(f"\nResponse:\n\t{response.response}\n")


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