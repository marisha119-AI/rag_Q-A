import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

CHROMA_DIR = "./chroma_db"
vectorstore = None

def load_document(file_path: str):
    global vectorstore
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return len(chunks)

def query_rag(question: str) -> str:
    global vectorstore
    if vectorstore is None:
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
    results = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer using ONLY the provided context. If not found, say 'I dont know based on the document.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content