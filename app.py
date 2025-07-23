#This is for local CLI testing

from file_processing import process_files
from vectorstore import build_vector_store
from chatbot import create_chatbot_chain
from document_builder import convert_to_langchain_documents
import os

def run_cli_chat():
    dir = 'pdfs'
    files = os.listdir(dir)
    print(files)
    
    file_dict = {}
    for file in files:
        file_path = os.path.join(dir, file)
        print(file_path)
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        file_dict[file]=file_bytes

    # Call process_files to extract all documents
    all_docs = process_files(file_dict)

    langchain_docs = convert_to_langchain_documents(all_docs)

    vector_store = build_vector_store(langchain_docs)
    chatbot = create_chatbot_chain(vector_store)

    print("📚 PDF Chatbot Ready. Ask your question (type 'exit' to quit):")
    while True:
        query = input("🗨️ You: ")
        if query.lower() == "exit":
            break
        response = chatbot.invoke({'question':query})
        print("\n🤖 Bot:", response['answer'])
        print("📎 Sources:")
        for doc in response["source_documents"]:
            print(f" - {doc.metadata['filename']}, Page {doc.metadata['page_number']}")
        print("-" * 60)
    

if __name__ == "__main__":
    run_cli_chat()