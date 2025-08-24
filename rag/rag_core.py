import os, pickle
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

base_folder = Path("C:/Law-bot/All_laws_categories")
processed_files_pickle = "C:/Users/aitoo/OneDrive/Desktop/Pak-Law/PakLawAI/data/processed_files.pkl"
collection_name = "first_Rag"
qdrant_url = "http://localhost:6333"

def load_processed_files():
    if os.path.exists(processed_files_pickle):
        with open(processed_files_pickle, "rb") as f:
            return pickle.load(f)
    return set()

def save_processed_files(processed_files):
    with open(processed_files_pickle, "wb") as f:
        pickle.dump(processed_files, f)

def load_new_pdfs(base_folder, processed_files):
    all_docs, new_files = [], []
    for pdf_file in Path(base_folder).rglob("*.pdf"):
        if str(pdf_file) not in processed_files:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            all_docs.extend(docs)
            new_files.append(str(pdf_file))
    return all_docs, new_files

def split_documents(docs, chunk_size=2000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

def create_or_connect_vector_store(documents, embeddings):
    if documents:
        return QdrantVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=collection_name,
            url=qdrant_url
        )
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        url=qdrant_url
    )
