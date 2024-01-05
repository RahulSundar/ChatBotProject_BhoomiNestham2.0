import os, sys
import time
import openai
import logging
import streamlit as st

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

SECRET_API_TOKEN = os.environ["SECRET_TOKEN"]
os.environ["OPENAI_API_KEY"] = SECRET_API_TOKEN
openai.api_key = os.environ["OPENAI_API_KEY"]


@st.cache_resource
def indexgenerator(indexPath, documentsPath):

    # check if storage already exists
    if not os.path.exists(indexPath):
        print("Not existing")
        # load the documents and create the index
        documents = SimpleDirectoryReader(documentsPath).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(indexPath)
    else:
        # load the existing index
        print("Existing")
        storage_context = StorageContext.from_defaults(persist_dir=indexPath)
        index = load_index_from_storage(storage_context)
        
    return index
