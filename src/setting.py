import glob

from langchain.docstore.document import Document
from langchain_community.document_loaders import BSHTMLLoader
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)


def get_es_docs() -> list[Document]:
    docs: list[Document] = []
    files = glob.glob("./src/assets/*.html")

    for file in files:
        loader = BSHTMLLoader(file)
        docs += text_splitter.split_documents(loader.load())

    return docs

from decouple import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.elasticsearch import ElasticsearchStore

# 環境変数読み込み
OPENAI_API_KEY = config("OPENAI_API_KEY")
INDEX_NAME = config("INDEX_NAME")
ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_store = ElasticsearchStore(
    es_url=ELASTICSEARCH_HOST,
    index_name=INDEX_NAME,
    embedding=embeddings,
    strategy=ElasticsearchStore.ExactRetrievalStrategy()
)

from langchain_openai import ChatOpenAI

def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)


def get_vector_store() -> ElasticsearchStore:
    return vector_store


def create_index(vector_store: ElasticsearchStore):
    docs = get_es_docs()
    print("=== add documents to index ===")
    vector_store.add_documents(
        docs,
        bulk_kwargs={
            "chunk_size": 500,
            "max_chunk_bytes": 50000000,
        }
    )


if __name__ == "__main__":
    create_index(vector_store)
