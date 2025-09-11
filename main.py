from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from dotenv import load_dotenv

load_dotenv()

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

directory_loader = DirectoryLoader("./docs", glob="*.pdf")


vector_store = Chroma(
    collection_name='docs',
    embeddings=gemini_embeddings,
    persist_directory='./chroma_db',
)