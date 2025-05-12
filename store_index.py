from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document


load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("medicalchatbot")


# Create a vector store

# vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Add the text chunks to the vector store
uuids = [str(uuid4()) for _ in range(len(text_chunks))]
vector_store = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name="medicalchatbot",
    ids=uuids
)



