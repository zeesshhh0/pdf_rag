from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import logging

log = logging.getLogger()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

directory_loader = PyPDFLoader(file_path="./docs/resume.pdf")

log.info("PDF Loaded now splitting...")

load_docs = directory_loader.lazy_load()

splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

chunked_docs = splitter.split_documents(load_docs)

log.info("Splitted now adding to vector store...")

vector_store = Chroma(
    collection_name='docs',
    embedding_function=gemini_embeddings,
    persist_directory='./chroma_db',
)

vector_store.add_documents(chunked_docs)

log.info("Added to vector store...")