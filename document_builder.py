from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


def convert_to_langchain_documents(extracted_docs: list[dict]) -> list[Document]:
    """
        Converts List of dict into LangChain Document objects with metadata.
        Each dict must have: (text, filename, page_number)
        """
    docs = []
    for doc in extracted_docs:
        if doc['text'].strip():  # avoid empty pages
            docs.append(Document(
                page_content=doc['text'],
                metadata={
                    "filename": doc['filename'],
                    "page_number": doc['page_number']
                    }
            ))

          
        
    return docs
