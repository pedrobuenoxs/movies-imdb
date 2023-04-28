import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import PINECONE_API_KEY, OPENAI_API_KEY
import argparse

# Initialize Pinecone
def init_pinecone(api_key, environment):
    pinecone.init(api_key=api_key, environment=environment)

# Load documents from the directory
def load_documents(path, glob_pattern):
    loader = DirectoryLoader(path, glob=glob_pattern)
    return loader.load()

# Split documents into chunks
def split_documents(texts, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.transform_documents(texts)

# Create a Pinecone vectorstore from documents and embeddings
def create_docsearch(index_name, namespace, docs, embeddings):
    return Pinecone.from_documents(docs, embeddings, index_name=index_name, namespace=namespace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data and create a Pinecone vectorstore")
    parser.add_argument("namespace", help="Namespace for the vectorstore")
    args = parser.parse_args()
    # Set up Pinecone and OpenAI API keys
    pinecone_api_key = PINECONE_API_KEY
    openai_api_key = OPENAI_API_KEY
    init_pinecone(api_key=pinecone_api_key, environment="eu-west1-gcp")
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Load and process documents
    print("Loading documents...")
    path = os.path.join(os.path.dirname(__file__), "../content/")
    texts = load_documents(path, glob_pattern="**/*.txt")
    print("Splitting documents...")
    docs = split_documents(texts, chunk_size=2000, chunk_overlap=0)

    # Create embeddings and vectorstore
    embeddings = OpenAIEmbeddings()
    print("Creating vectorstore...")
    docsearch = create_docsearch(index_name="imdb", namespace=args.namespace, docs=docs, embeddings=embeddings)
    print("Done!")