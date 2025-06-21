import pandas as pd
import numpy as np
import fastapi
import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from contextlib import asynccontextmanager
from langchain_qdrant import QdrantVectorStore
from applicationLayer import Retriver
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from Clients.JwksClient import JwksClient

load_dotenv()
MODEL_URL = os.environ['MODEL_URL']
MODEL_PASS = os.environ['MODEL_PASS']
FRONTEND_PATH = os.environ["FRONTEND_PATH"]

# Instantiate JwksClient with the JWKS URI for your Azure AD tenant
jwks_client = JwksClient()


async def load_model():
    global llm, hf_embed
    llm = AzureChatOpenAI(azure_endpoint="https://agr-openai-dev-eu2.openai.azure.com/",
                    azure_deployment="gpt-4o-mini",
                    openai_api_key=os.environ.get('API_KEY'),
                    openai_api_version="2024-07-01-preview",
                    temperature=0,
                    timeout=120)
    hf_embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    print('model loaded')


async def load_db():
    global vector_store_from_client,retriever
    vector_store_from_client = QdrantVectorStore.from_existing_collection(
    embedding=hf_embed,
    collection_name="demo_collection",
    url=MODEL_URL,
    api_key=MODEL_PASS,
    port=None)

    retriever=Retriver(llm,vector_store_from_client).retriever()
    print('vector db loaded')


@asynccontextmanager
async def lifespan(app:FastAPI):
    await load_model()
    await load_db()
    yield


# pydantic model to define input
class RequestModel(BaseModel):
    text:str

app=FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve React static files
app.mount("/static", StaticFiles(directory=f"{FRONTEND_PATH}/build/static"), name="static")

# Serve the React index.html file
@app.get("/")
async def serve_react_app():
    return FileResponse(f"{FRONTEND_PATH}/build/index.html")

@app.post("/api/similar_items")
async def predict(request: RequestModel,token_payload=Depends(jwks_client.validate_token)):
    global retriever
    return retriever.invoke(request.text)