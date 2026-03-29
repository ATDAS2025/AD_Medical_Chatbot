
from langchain.document_loaders import PyPDFLoader,DirectoryLoader  ## Required for loading the PDF files and Directory
from langchain.text_splitter import RecursiveCharacterTextSplitter  ## Required for Chunking opertion
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings


def load_pdf_files(data):
    """
    This function is used to load the PDF files from the given directory and return the documents.
    """
    loader = DirectoryLoader(data, glob="*.pdf", show_progress=True, loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    This function is used to filter the documents to only include the content and metadata.
    """
    minimal_docs : List[Document]= []
    for doc in docs:
        src = doc.metadata.get("source", "unknown_source")
        minimal_doc = Document(
            page_content=doc.page_content,
            metadata= {"source": src}
        )
        minimal_docs.append(minimal_doc)
    return minimal_docs

##Split the documents into smaller chunks using RecursiveCharacterTextSplitter
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500
                                                   , chunk_overlap=20)
    split_docs = text_splitter.split_documents(minimal_docs)
    return split_docs

## This function is used to download the embeddings from HuggingFace and return the embeddings object.
def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings