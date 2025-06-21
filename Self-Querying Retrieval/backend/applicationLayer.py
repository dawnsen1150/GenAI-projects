from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import (
    StructuredQueryOutputParser,
    get_query_constructor_prompt,
    load_query_constructor_runnable
)
from langchain_qdrant import QdrantVectorStore
# from langchain.retrievers.self_query.qdrant import QdrantTranslator
from langchain_community.query_constructors.qdrant import QdrantTranslator


class Retriver:
    def __init__(self,llm,vectorStore):
        self.llm=llm
        self.vector=vectorStore


    def retriever(self):  
        metadata_field_info = [
        AttributeInfo(
            name="item_number",
            description="The item_number is the unique identifier for each furniture",
            type="string",
        ),
        AttributeInfo(
            name="type",
            description="The type is the type of the furniture ",
            type="string",
        ),
        AttributeInfo(
            name="color",
            description="The color of the furniture",
            type="string",
        ),
        AttributeInfo(
            name="depth", description="depth of the furniture", type="float"
        ),
        AttributeInfo(
            name="height", description="height of the furniture", type="float"
        ),
        AttributeInfo(
            name="width", description="weight of the furniture", type="float"
        ),
        AttributeInfo(
            name="price", description="price of the furniture", type="float"
        ),
        AttributeInfo(
            name="style",
            description="The style of the furniture",
            type="string",
        ),
        AttributeInfo(
            name="url", description="image url of the furniture", type="string"
        ),]
        document_content_description = "Description of the furniture. Furniture can be different based on the description. For example,'dresser' is different from 'dresser and mirror'. "
        
        chain = load_query_constructor_runnable(self.llm, document_contents=document_content_description,attribute_info=metadata_field_info,enable_limit=True)
        prompt = get_query_constructor_prompt(
        document_content_description,
        metadata_field_info,
        enable_limit=True
        )
        output_parser = StructuredQueryOutputParser.from_components()
        query_constructor = prompt | self.llm | output_parser

        retriever = SelfQueryRetriever(
            query_constructor=query_constructor,
            vectorstore=self.vector,
            structured_query_translator=QdrantTranslator(metadata_key="metadata"),
            search_kwargs={"k": 20000}
        )

        return retriever

