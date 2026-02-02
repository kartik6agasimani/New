from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

loader = PyPDFLoader("KBB.pdf")  
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(pages)

embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(docs, embeddings)

retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

st.title("Chat with your PDF")

query = st.text_input("Ask a question about the document:")

if query:
    result = qa({"query": query})
    st.write(result["result"])
