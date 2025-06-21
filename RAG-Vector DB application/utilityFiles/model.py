from pydantic import BaseModel, Field

# pydantic model to define input
class RequestModel(BaseModel):
    text:str