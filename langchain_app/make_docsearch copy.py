from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
prompt_template = """
You are a movie critic who lives and breathes movies. 
You previously worked with Buzzfeed, Imdb and Blockbuster. 
You are easily excitable and extremely passionate about movies.

In 300 words, Compare the movie {Child} with {Parent} to someone who just watched {Parent}. 
Explain how {child} is similar to {parent} - cultural, thematic, plot, vibe?"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["Child", "Parent"]
)

llm = OpenAI(temperature=0)

chain = LLMChain(llm=llm, prompt=PROMPT)

source_chunks = []
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source in sources:
    for chunk in splitter.split_text(source.page_content):
        source_chunks.append(Document(page_content=chunk, metadata=source.metadata))

def generate_blog_post(topic):
    search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings())
    docs = search_index.similarity_search(topic, k=4)
    inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
    print(chain.apply(inputs))