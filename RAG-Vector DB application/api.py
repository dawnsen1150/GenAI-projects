import pandas as pd
import numpy as np
import fastapi
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import datetime as dt
import requests
import os
from dotenv import load_dotenv
from utilityFiles.applicationLayer import ChatBot
from utilityFiles.llm_client import get_llm_client, get_embeddings_client, get_vector_store
from fastapi.responses import FileResponse
from utilityFiles.model import RequestModel
import uvicorn

# Load environment variables from .env file
load_dotenv()
# FRONTEND_PATH = os.environ["FRONTEND_PATH"]

async def load_model():
    global client, llm, chatbot, sys_prompt

    with open('prompt.txt', 'r') as file:
        sys_prompt = file.read()

    # LLM
    llm=get_llm_client()


    #embedding model
    hf_embed = get_embeddings_client()

    # connecting with vector database
    vector_store=get_vector_store()


    chatbot=ChatBot(model=llm,vector_store=vector_store,prompt=sys_prompt)

    print('model and vector db loaded')



# loading the necessary data before the api starts
@asynccontextmanager
async def lifespan(app:FastAPI):
    await load_model()
    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# # Serve React static files
# app.mount("/static", StaticFiles(directory=f"{FRONTEND_PATH}/build/static"), name="static")

# # Serve the React index.html file
# @app.get("/")
# async def serve_react_app():
#     return FileResponse(f"{FRONTEND_PATH}/build/index.html")

@app.get("/")
async def root():
    return {"message": "Tides chatbot API is up and running."}


@app.post("/tides_chatbot/q&a")
async def showing(request: RequestModel):
    global client, llm, chatbot,sys_prompt

    try:
        response = chatbot.generate_response(request.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app 
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)