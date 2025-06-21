from openai import AzureOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.azure_cosmos_db import (
    AzureCosmosDBVectorSearch,
    CosmosDBSimilarityType,
    CosmosDBVectorSearchType,
)
from pymongo import MongoClient
from functools import lru_cache
import os

@lru_cache(maxsize=10)
def get_llm_client():
    llm=AzureOpenAI(azure_endpoint=os.environ.get('azure_endpoint'),
                   api_key=os.environ.get('api_key'),
                   api_version=os.environ.get('api_version'))
    return llm
@lru_cache(maxsize=10)
def get_embeddings_client():
    hf_embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return hf_embed


@lru_cache(maxsize=10)
def get_vector_store():
    # connecting with vector database
    connectionString = os.environ.get('connection_string')
    database_name = "q&aPriya"
    collection_name = "myNewCollections"
    # index_name = "q&a"  # Not used in this function

    hf_embed = get_embeddings_client()  # Use the cached embeddings client

    vector_store = AzureCosmosDBVectorSearch.from_connection_string(
        connection_string=connectionString,
        namespace=f"{database_name}.{collection_name}",
        embedding=hf_embed,
    )
    return vector_store
