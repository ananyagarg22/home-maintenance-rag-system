from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import shutil
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['API_KEY']

CHROMA_PATH = "chromadb"
DATA_PATH = "documents"

def main():
    # print("I.Inside main")
    generate_data_store()

def generate_data_store():
    # print("II.Inside generate data store")
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    # print("IIIA.Inside load documents")
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", show_progress=True, loader_cls=PyPDFLoader)
    # print("Loader ready")
    documents = loader.load()
    # print("Documents loaded, returning them")
    return documents

def split_text(documents: list[Document]):
    # print("IIIB.Inside split text")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # document = chunks[10]
    # print(document.page_content)
    # print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # print("IIIC.Inside save to chroma")
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(api_key=API_KEY), persist_directory=CHROMA_PATH
    )
    # db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()