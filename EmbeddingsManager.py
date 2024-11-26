from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader



class EmbeddingsManager:
    """A class to manage embeddings in the vector store."""

    def __init__(self):

        # Load the API key from the .env file
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        if OPENAI_API_KEY:
            print("API key loaded successfully.")
        else:
            raise ValueError("Error loading API key. Check that OPENAI_API_KEY is set inside .env")
        
        self.vectorstore = Chroma(embedding_function=OpenAIEmbeddings, persist_directory="data")

    def add_embedding(self, document_id, content):

        try:
            self.vectorstore.add_texts([content], metadatas=[{"id": document_id}], ids=[document_id])
            print(f"Document '{document_id}' added to embeddings.")
        except Exception as e:
            print(f"Failed to add embedding for document '{document_id}': {str(e)}")

    def load_and_add_document(self, document_id, source):
        try:
            # Load PDF document
            loader = PyMuPDFLoader(source)

            # Load and split the document
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
            splits = text_splitter.split_documents(documents)

            # Add each split to the vector store
            for i, doc in enumerate(splits):
                split_id = f"{document_id}_part_{i+1}"
                self.add_embedding(split_id, doc.page_content)

            print(f"Document '{document_id}' loaded and added to embeddings.")
        except Exception as e:
            print(f"Failed to load and add document '{document_id}': {str(e)}")
