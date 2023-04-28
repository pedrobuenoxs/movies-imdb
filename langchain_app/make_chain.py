from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
import pinecone
from langchain import VectorDBQA, OpenAI
from langchain.chains import RetrievalQA
from config import PINECONE_API_KEY, OPENAI_API_KEY
#initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment="eu-west1-gcp"  # next to api key in console
)

# configure your openai api key
import os
os.environ[OPENAI_API_KEY] = OPENAI_API_KEY

embeddings = OpenAIEmbeddings()

docsearch = Pinecone.from_existing_index( index_name="amboss-qa",embedding=embeddings, namespace="file-x")



# # create the chain
chain = RetrievalQA.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever(),return_source_documents=True)


def make_chain_with_parameters(index_name, namespace, query):
    embeddings = OpenAIEmbeddings()

    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings, namespace=namespace)

    chain = RetrievalQA.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)

    return chain({"query": query})
