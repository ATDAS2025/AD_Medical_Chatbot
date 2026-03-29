from dotenv import load_dotenv
import os
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()  ## This will load the environment variables from the .env file

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  ## This will get the Pinecone API key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  ## This will get the OpenAI API key from the environment variables

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY  ## This will set the Pinecone API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  ## This will set the OpenAI API key as an environment variable

extracted_data = load_pdf_files("data/")  ## This is the directory where the PDF files are stored
minimal_docs = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(minimal_docs)

embeddings = download_embeddings()  ## This will download the embeddings from HuggingFace

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)

index_name = "ad-medical-chatbot"  ## This is the name of the Pinecone index that we will create
if not pc.has_index(index_name):
    pc.create_index(name=index_name
                    , dimension=384
                    , metric="cosine"
                    , spec=ServerlessSpec(cloud="aws"
                                         , region="us-east-1"))
index = pc.Index(index_name)  ## This will create an index object for the Pinecone index created above

docsearch = PineconeVectorStore.from_documents(documents=text_chunks,
                                               embedding=embeddings,
                                               index_name=index_name)  ## This will create a PineconeVectorStore object from the documents, embeddings and index name provided  

