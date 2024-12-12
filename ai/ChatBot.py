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
    def __init__(self, user_id, course_id):
        # Load the API key from the .env file
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        if OPENAI_API_KEY:
            print("API key loaded successfully.")
        else:
            raise ValueError("Error loading API key. Check that OPENAI_API_KEY is set inside .env")
        
        self.user_id = user_id
        self.course_id = course_id
        
        # STATIC ATTRIBUTES
        # creo que corpus no es necesario
        CHROMA_PATH = "data"  # Default to a "data" folder in the current working directory

        # INSTANCE ATTRIBUTES
        self.chat_history = []  # Store chat history as a list of {"question": ..., "answer": ...}

        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=OPENAI_API_KEY)

        # os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        # Load the existing ChromaDB from the "data" directory and set it as the retriever
        #TODO meter trycatch
        self.vectorstore = Chroma(persist_directory="data", embedding_function=OpenAIEmbeddings())

        self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={
            "k": 5,  # Number of results to retrieve
            "filter": {
                "$and": [
                    {"user_id": self.user_id},
                    {"course_id": self.course_id}
                ]
            }
        })
        
        # PROMPTING
        self.prompt = PromptTemplate(
            input_variables=["history", "context", "question"],
            template = """
            You are a helpful and knowledgeable assistant. Please answer the question based strictly on the provided information. 
            If the answer is not in the provided context, say: "I couldn't find the answer in the provided information. Could you clarify or provide more details?"

            Here's our conversation so far:
            {history}

            Here's the context I found for you:
            {context}

            Now, here's the question:
            {question}

            Based on the context, here's my answer:
            """
        )

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

        response = rag_chain.invoke(question)
        # Update chat history with the latest interaction
        self.chat_history.append({"question": question, "answer": response})

        return response

def main():
    # Instantiate the chatbot with user-specific and course-specific filters
    chatbot = ChatBot(user_id="user123", course_id="course456")

    # Ask a question
    response = chatbot.answer("Tell me a good example of paper structure.")
    print("======================================")
    print(response)

    response = chatbot.answer("Say that but more concise.")
    print("======================================")
    print(response)

    response = chatbot.answer("Explain that last part a bit more in detail.")
    print("======================================")
    print(response)

    response = chatbot.answer("What is Dragon Ball Z?")
    print("======================================")
    print(response)

if __name__ == "__main__":
    main()