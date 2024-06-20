from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# Import necessary modules

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Print a message to indicate the start of the ingestion process
    print("Ingesting...")

    # Load the text from the "questions.txt" file using the TextLoader
    loader = TextLoader("questions.txt", encoding='utf-8')
    document = loader.load()

    # Print a message to indicate the start of the splitting process
    print("Splitting...")

    # Split the document into smaller chunks using the CharacterTextSplitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)

    # Print the number of chunks created
    print(f"Created {len(texts)} chunks")

    # Initialize the GoogleGenerativeAIEmbeddings with the specified model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Print a message to indicate the start of the ingestion process
    print("Ingesting...")

    # Ingest the text chunks into the PineconeVectorStore
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )

    # Print a message to indicate the completion of the ingestion process
    print("Finish")