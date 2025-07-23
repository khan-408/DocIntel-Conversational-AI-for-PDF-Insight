import streamlit as st
from file_processing import process_files
from document_builder import convert_to_langchain_documents
from vectorstore import build_vector_store
from chatbot import create_chatbot_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os


st.set_page_config(page_title="📚PDF Chatbot", page_icon="🤖", layout="centered")
# Sidebar: File Upload
# ------------------------------------------
st.sidebar.title("📁 Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Select PDF files", type=["pdf"], accept_multiple_files=True)

# ------------------------------------------
# Chatbot Initialization
# ------------------------------------------
if "chatbot" not in st.session_state and uploaded_files:
    file_dict = {file.name: file.read() for file in uploaded_files}
    extracted_docs = process_files(file_dict)
    langchain_docs = convert_to_langchain_documents(extracted_docs)

    # Optional: Split and embed inside build_vector_store
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(langchain_docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embedding=embeddings)

    st.session_state.chatbot = create_chatbot_chain(vector_store)
    st.session_state.chat_history = []
    st.success("🔗 PDFs processed and chatbot is ready!")

# ------------------------------------------
# Main Chat Interface
# ------------------------------------------
st.title("🤖 Ask Your PDFs Anything")

query = st.chat_input("Type your question...")

if query and "chatbot" in st.session_state:
    with st.spinner("Thinking..."):
        response = st.session_state.chatbot.invoke({"question": query})
        st.session_state.chat_history.append(
            {"question": query, "answer": response["answer"], "sources": response["source_documents"]}
        )

# ------------------------------------------
# Display Chat History
# ------------------------------------------
if "chat_history" in st.session_state:
    for item in st.session_state.chat_history:
        st.markdown(f"🟦 **You:** {item['question']}")
        st.markdown(f"🟨 **Bot:** {item['answer']}")
        with st.expander("📎 Sources", expanded=False):
            for doc in item["sources"]:
                st.markdown(
                    f"🔹 **{doc.metadata['filename']}** — Page `{doc.metadata['page_number']}`",
                    help=doc.page_content[:250] + "..."
                )
        st.divider()
