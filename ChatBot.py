import os
from dotenv import load_dotenv
from langchain_chroma import Chroma

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import PromptTemplate



class ChatBot():
    """Class for the RAG Chatbot for Chat. This class contains methods for managing embeddings,
    and generating answers to questions, with customizable behavior."""
    def __init__(self):
        # Load the API key from the .env file
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        if OPENAI_API_KEY:
            print("API key loaded successfully.")
        else:
            raise ValueError("Error loading API key. Check that OPENAI_API_KEY is set inside .env")
        
        # STATIC ATTRIBUTES
        # creo que corpus no es necesario
        CORPUS_PATH = os.path.join(os.getcwd(), "corpus")  # Default to a "corpus" folder in the current working directory
        CHROMA_PATH = os.path.join(os.getcwd(), "data")  # Default to a "data" folder in the current working directory

        # INSTANCE ATTRIBUTES
        self.session_id = 0
        self.chat_history = []  # Store chat history as a list of {"question": ..., "answer": ...}

        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

        # os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        # Load the existing ChromaDB from the "data" directory and set it as the retriever
        #TODO meter trycatch
        self.vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
        self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

        #TODO crear dictionary enumerate con las diferentes prompts
        # PROMPTING
        self.prompt = PromptTemplate(
            input_variables=["history", "context", "question"],
            template="""
            You are a knowledgeable assistant. Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

            Conversation history:
            {history}

            Context:
            {context}

            Question:
            {question}

            Answer:
        """)

        print("ChatBot initialized successfully!")
        
    def format_docs(self, docs):
        """Format the retrieved documents into a single context string for the prompt."""
        return "\n\n".join(doc.page_content for doc in docs)
    
    def format_history(self):
        """Format the chat history into a string for inclusion in the prompt."""
        return "\n".join(
            f"Q: {item['question']}\nA: {item['answer']}" for item in self.chat_history[-3:]
        )

    def answer(self, question):
        """Generate an answer using the RAG chain."""
        # Define the RAG chain using LCEL
        rag_chain = (
            {
                "history": RunnableLambda(lambda _: self.format_history()),  # Retrieve formatted history
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            # | StrOutputParser()
            | RunnableLambda(lambda x: x.content)  # Extracts content from the model's output
        )

        # for chunk in rag_chain.stream(question):
        #     print(chunk, end="", flush=True)
        # print("\n\n")

        response = rag_chain.invoke(question)
        # Update chat history with the latest interaction
        self.chat_history.append({"question": question, "answer": response})

        return response

    
        
if __name__ == "__main__":
    bot = ChatBot()
    print("====================================================")
    print(bot.answer("Hello!"))
    print(bot.answer("Tell me what year America was discovered."))
