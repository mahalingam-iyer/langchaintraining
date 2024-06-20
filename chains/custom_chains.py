from langchain_core.runnables import RunnableSequence
from langchain.prompts.prompt import PromptTemplate
from output_parsers import expertise_parser
from langchain_google_genai import GoogleGenerativeAI
import os

# Create an instance of the GoogleGenerativeAI class with the "gemini-pro" model
llm = GoogleGenerativeAI(model="gemini-pro")

def get_expertise_chain() -> RunnableSequence:
    """
    This function returns a RunnableSequence that represents a chain used to get the expertise of a person.

    Returns:
        RunnableSequence: The chain to get the expertise of a person.
    """

    # Define the expertise template
    expertise_template = """given the information about a person from linkedin {information} I want you to get me his technical expertise of the person is he more suitable as Java developer or JavaScript developer
                            Answer should have two parts
                            part one is a string either Java or JavaScript or Do not know 
                            and part two interger of number of years of experience in the technology
                            \n{format_instructions}"""

    # Create a PromptTemplate object with the expertise template
    expertise_prompt_template = PromptTemplate(
        template=expertise_template,
        input_variables=["information"],
        partial_variables={
            "format_instructions": expertise_parser.get_format_instructions()
        },
    )

    # Create the chain by combining the expertise_prompt_template, llm, and expertise_parser
    return expertise_prompt_template | llm | expertise_parser