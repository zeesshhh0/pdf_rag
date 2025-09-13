import chainlit as cl

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import  PromptTemplate
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@cl.on_chat_start
async def start():
  
  vector_store = Chroma(
    collection_name="pdf_rag_chat",
    embedding_function=embeddings,
    persist_directory='./chroma_db'
  )
  
  files = None
  while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a pdf file to begin!",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
            max_files=1
        ).send()

  file = files[0]

  msg = cl.Message(content=f"Processing `{file.name}`...")
  await msg.send()
  
  pdf_loader = PyPDFLoader(file.path)

  docs = pdf_loader.lazy_load()
  
  chunked_docs = text_splitter.split_documents(docs)

  vector_store.reset_collection()

  await vector_store.aadd_documents(chunked_docs)
  
  msg2 = cl.Message(content=f"done processing `{file.name}`...")
  await msg2.send()

@cl.on_chat_end
async def on_chat_end():
  vector_store = Chroma(
    collection_name="pdf_rag_chat",
    embedding_function=embeddings,
    persist_directory='./chroma_db'
  )
  await vector_store.delete_collection()


@cl.on_message
async def main(message):
  vector_store = Chroma(
    collection_name="pdf_rag_chat",
    embedding_function=embeddings,
    persist_directory='./chroma_db'
  )
  
  docs = await vector_store.asimilarity_search(message.content, k=2)
  
  prompt= PromptTemplate(
    template="""
    You are a Helpfull assistant that helps people find information in a pdf file.
    \n\n
    Context: {context}
    Question: {question}
    \n\n
    Answer:
    """,
    input_variables=["context", "question"]
  )
  
  formatted_prompt = prompt.format(context=docs[0].page_content, question=message.content)
  
  response = await llm.ainvoke(formatted_prompt)
  
  await cl.Message(content=response.content).send()