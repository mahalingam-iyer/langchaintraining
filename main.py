from langchain_google_genai import GoogleGenerativeAI  # Importing the GoogleGenerativeAI class from langchain_google_genai module
from langchain_pinecone import PineconeVectorStore  # Importing the PineconeVectorStore class from langchain_pinecone module
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Importing the GoogleGenerativeAIEmbeddings class from langchain_google_genai module
from typing import Tuple  # Importing the Tuple class from typing module
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent  # Importing the lookup function from agents.linkedin_lookup_agent module and aliasing it as linkedin_lookup_agent
from output_parsers import Expertise  # Importing the Expertise class from output_parsers module
from third_parties.linkedin import scrape_linkedin_profile  # Importing the scrape_linkedin_profile function from third_parties.linkedin module
import os  # Importing the os module
from chains.custom_chains import get_expertise_chain  # Importing the get_expertise_chain function from chains.custom_chains module
from langchain import hub  # Importing the hub module from langchain package
from langchain.chains.combine_documents import create_stuff_documents_chain  # Importing the create_stuff_documents_chain function from langchain.chains.combine_documents module
from langchain.chains.retrieval import create_retrieval_chain  # Importing the create_retrieval_chain function from langchain.chains.retrieval module
import proto.marshal.collections.repeated  # Importing the proto.marshal.collections.repeated module

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
    """
    Finds questions for a given user's name.

    Args:
        name (str): The name of the user.

    Returns:
        str: The result of the retrieval chain.
    """
    linkedin_username = linkedin_lookup_agent(name=name)  # Look up the LinkedIn username using the name
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)  # Scrape the LinkedIn profile using the LinkedIn username
    expertise_chain = get_expertise_chain()  # Get the expertise chain
    expertise: Expertise = expertise_chain.invoke(input={"information": linkedin_data})  # Invoke the expertise chain with the LinkedIn data
    print(expertise.expertise)  # Print the expertise
    print(expertise.years_of_experience)  # Print the years of experience
    embeddings = SerializedGoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Create an instance of SerializedGoogleGenerativeAIEmbeddings with the specified model
    llm = GoogleGenerativeAI(model="gemini-pro")  # Create an instance of GoogleGenerativeAI with the specified model
    vectorstore = PineconeVectorStore(index_name=os.environ["INDEX_NAME"], embedding=embeddings)  # Create an instance of PineconeVectorStore with the specified index name and embeddings
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")  # Pull the retrieval QA chat prompt from the hub
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)  # Create the combine documents chain with the specified llm and retrieval QA chat prompt
    retrieval_chain = create_retrieval_chain(retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain)  # Create the retrieval chain with the specified retriever and combine documents chain
    result = retrieval_chain.invoke(input={"input": f"{expertise.expertise} questions for {expertise.years_of_experience} years experienced developer"})  # Invoke the retrieval chain with the input
    print(result)  # Print the result

if __name__ == "__main__":
    find_questions_for_user("mahalingam iyer, full stack developer working at Innominds software")  # Call the find_questions_for_user function with the specified name