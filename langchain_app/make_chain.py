from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain import OpenAI
from langchain.chains import RetrievalQA
from config import PINECONE_API_KEY, OPENAI_API_KEY
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from make_docsearch import docsearch

prompt_template = """
You are a movie critic who lives and breathes movies. 
You previously worked with Buzzfeed, Imdb and Blockbuster. 
You are easily excitable and extremely passionate about movies.

Context: {context}

In 2 paragraphs, compare the movie {Child} with {Parent} to someone who just watched {Parent}. 
Explain how {Child} is similar to {Parent} - cultural, thematic, plot, vibe, etc.
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["Child", "Parent", "context"]
)

llm = OpenAI(temperature=0)

chain = LLMChain(llm=llm, prompt=PROMPT)


def generate_blog_post(parent, childs):
    docs_parents = docsearch.similarity_search(parent, k=4)
    docs_childs = [docsearch.similarity_search(child, k=4) for child in childs]
    # for doc in docs_parents:
    #     print("PARENTS")
    #     print(doc)
    # for doc in docs_childs:
    #     print("CHILDREN")
    #     print(doc[0])

    inputs = [{"context": doc.page_content + docs_c[0].page_content, "Child": child, "Parent": parent} for doc, docs_c, child in zip(docs_parents, docs_childs, childs)]
    print(inputs)

    # print(chain.apply(inputs))

generate_blog_post("Interstellar", ["Gravity", "Moon", "Passengers", "The Andromeda Strain", "The Grey", "The Martian", "The Revenant", "The Road", "The Survivalist"])