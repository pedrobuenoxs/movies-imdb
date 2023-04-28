from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import PINECONE_API_KEY, OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment="eu-west1-gcp"  # next to api key in console
)


embeddings = OpenAIEmbeddings()

docsearch = Pinecone.from_existing_index( index_name="imdb",embedding=embeddings, namespace="all_movies2")

