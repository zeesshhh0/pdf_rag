from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

user_query = input("Query: ")

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

llm = GoogleGenerativeAI(model="gemini-2.5-flash")

vector_store = Chroma(
  collection_name="docs",
  embedding_function=gemini_embeddings,
  persist_directory='./chroma_db'
) 

retriever = vector_store.as_retriever(
  search_type='similarity',
  search_kwargs={'k': 3}
  )

prompt = PromptTemplate(
  template="You are an Resume AI chatbot. Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer. \n\nContext:{context}\n\nQuestion: {question}\nAnswer:",
  input_variables=["context", "question"]
)

relevent_docs = retriever.invoke(user_query)

formated_prompt = prompt.format(context="\n\n".join([doc.page_content for doc in relevent_docs]), question=user_query)

response = llm.invoke(formated_prompt)

print(response)