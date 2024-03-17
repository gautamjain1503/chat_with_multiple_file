import os
import pinecone
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve necessary environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key in environment
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Function for ingesting data from files
def data_ingestion(paths: list):
    # Initialize document loader with file paths
    loader = UnstructuredFileLoader(paths)
    # Load documents from files
    documents = loader.load()
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    # Split documents into smaller text chunks
    texts = text_splitter.split_documents(documents)
    
    return texts

# Function for creating embeddings and building Pinecone index
def embedding_db(texts):
    # Initialize OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
    # Initialize Pinecone with API key and environment
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    # Create Pinecone index from documents and embeddings
    doc_db = Pinecone.from_documents(
        texts,
        embeddings, 
        index_name='demo'
    )
    return doc_db
    
# Function for retrieving answers to queries
def retrieval_answer(query, doc_db):
    # Initialize ChatOpenAI for language model
    llm = ChatOpenAI()
    # Initialize RetrievalQA with language model and Pinecone retriever
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type='stuff',
        retriever=doc_db.as_retriever(),
    )
    # Run query against QA system
    result = qa.run(query)
    return str(result)

# Main chatbot function
def chatbot(paths: list, question :str) -> str:
    # Ingest data from files
    texts = data_ingestion(paths)
    # Create embeddings and build Pinecone index
    doc_db = embedding_db(texts)
    # Retrieve answer to the question
    answer = retrieval_answer(question, doc_db)
    return answer