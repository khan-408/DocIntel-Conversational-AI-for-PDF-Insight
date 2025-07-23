from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')


def create_chatbot_chain(vector_store):
    memory = ConversationBufferMemory(memory_key="chat_history",
                                    return_messages=True,
                                    input_key="question",      
                                    output_key="answer" 
                                    )
    model = ChatGroq(
            api_key = groq_api_key,
            model = 'llama3-8b-8192'
            ) 
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True
    )
    return qa_chain