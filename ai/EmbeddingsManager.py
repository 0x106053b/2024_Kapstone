import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


class EmbeddingsManager:
    """A class to manage embeddings in the vector store, including loading and splitting documents."""

    def __init__(self):
        """
        Initialize the manager and the vector store.
        :param persist_directory: Directory where embeddings are persisted.
        :param chunk_size: Size of each document chunk.
        :param chunk_overlap: Overlap between chunks.
        """
        # Load the API key from the .env file
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        if OPENAI_API_KEY:
            print("API key loaded successfully.")
        else:
            raise ValueError("Error loading API key. Check that OPENAI_API_KEY is set inside .env")

        # Initialize the vector store
        self.vectorstore = Chroma(
            embedding_function=OpenAIEmbeddings(),
            persist_directory="data",
        )

        # Initialize the text splitter
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)

    def process_file(self, file_path, user_id, course_id):
        """
        Process a single PDF file: load, split, and add to the vector store.
        :param file_path: Path to the PDF file.
        :param user_id: ID of the user uploading the file.
        :param course_id: ID of the course the file belongs to.
        """
        try:
            # Extract document_id from the file name
            document_id = os.path.splitext(os.path.basename(file_path))[0]
            print(f"Processing file: {file_path} (Document ID: {document_id})")

            # Load the document
            loader = PyPDFLoader(file_path=file_path)
            documents = loader.load()

            # Split the document
            splits = self.splitter.split_documents(documents)

            # Add splits to the vector store
            self.vectorstore.add_texts(
                [doc.page_content for doc in splits],
                metadatas=[
                    {"id": f"{document_id}_part_{i+1}", "user_id": user_id, "course_id": course_id}
                    for i in range(len(splits))
                ],
                ids=[f"{document_id}_part_{i+1}" for i in range(len(splits))],
            )

            print(f"File '{file_path}' processed successfully for user_id: {user_id}, course_id: {course_id}.")
        except Exception as e:
            print(f"Failed to process file '{file_path}': {str(e)}")

def main():
    # Initialize the EmbeddingsManager
    manager = EmbeddingsManager()

    # File details
    test_file = os.path.join(os.getcwd(), "pdfs", 'W07-2_Paper-structures1.pdf')

    user_id = "user123"
    course_id = "course456"

    # Process the test file
    print("Processing the test file...")
    manager.process_file(file_path=test_file, user_id=user_id, course_id=course_id)

    # Query the vector store to print entries for the user and course
    print("\nContents of the vector store filtered by user and course:")
    try:
        # Perform similarity search (use a dummy query to fetch all entries)
        results = manager.vectorstore.similarity_search(query="*", k=1000)

        # Filter results based on user_id and course_id
        filtered = [
            {"text": doc.page_content, "metadata": doc.metadata}
            for doc in results
            if doc.metadata.get("user_id") == user_id and doc.metadata.get("course_id") == course_id
        ]

        for entry in filtered:
            print(entry)
    except Exception as e:
        print(f"Error retrieving from vector store: {e}")


if __name__ == "__main__":
    main()
