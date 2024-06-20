from langchain_google_genai import GoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import Expertise
from third_parties.linkedin import scrape_linkedin_profile
import os
from chains.custom_chains import (
    get_expertise_chain,
)
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import proto.marshal.collections.repeated

def serialize_embedding(embedding):
    """
    Convert proto.marshal.collections.repeated.Repeated to a list.
    """
    if isinstance(embedding, proto.marshal.collections.repeated.Repeated):
        embedding = list(embedding)
    # Verify the embedding format
    if not isinstance(embedding, list):
        raise TypeError("Embedding should be a list")
    if not all(isinstance(x, (float, int)) for x in embedding):
        raise TypeError("Embedding should contain numerical values")
    return embedding

class SerializedGoogleGenerativeAIEmbeddings:
    def __init__(self, model):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=model)

    def embed_query(self, text):
        raw_embedding = self.embeddings.embed_query(text)
        serialized_embedding = serialize_embedding(raw_embedding)
        return serialized_embedding

def find_questions_for_user(
    name: str,
) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    expertise_chain = get_expertise_chain()
    expertise: Expertise = expertise_chain.invoke(input={"information": linkedin_data})
    print(expertise.expertise)
    print(expertise.years_of_experience)
    embeddings = SerializedGoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = GoogleGenerativeAI(model="gemini-pro")
    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrival_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )
    result = retrival_chain.invoke(input={"input": f"{expertise.expertise} questions for {expertise.years_of_experience} years experienced developer"})
    print(result)


if __name__ == "__main__":
    find_questions_for_user("mahalingam iyer, full stack developer working at Innominds software")