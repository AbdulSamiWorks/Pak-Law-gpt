from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from .rag_core import load_processed_files, save_processed_files, load_new_pdfs, split_documents, create_or_connect_vector_store, base_folder
from .prompts import build_system_prompt

# Init RAG
processed_files = load_processed_files()
all_docs, new_files = load_new_pdfs(base_folder, processed_files)
split_docs = split_documents(all_docs)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = create_or_connect_vector_store(split_docs, embeddings)
processed_files.update(new_files)
save_processed_files(processed_files)

def query_ai(system_prompt, user_query):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    return llm.invoke(messages).content

def ask_rag(user_query: str) -> str:
    search_results = vector_store.similarity_search(query=user_query)
    if not search_results:
        return "No relevant law found. Please ask something else."
    system_prompt = build_system_prompt(context=search_results)
    return query_ai(system_prompt, user_query)
