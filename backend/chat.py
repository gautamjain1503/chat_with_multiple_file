import os
import pinecone
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def data_ingestion(paths: list):
    loader=UnstructuredFileLoader(paths, )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    
    return texts

def embedding_db(texts):
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    doc_db = Pinecone.from_documents(
        texts,
        embeddings, 
        index_name='demo'
    )
    return doc_db
    
def retrieval_answer(query, doc_db):
    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type='stuff',
        retriever=doc_db.as_retriever(),
    )
    query = query
    result = qa.run(query)
    return str(result)


def chatbot(paths: list, question :str)-> str:
    texts=data_ingestion(paths)
    doc_db = embedding_db(texts)
    ans=retrieval_answer(question, doc_db)
    return ans