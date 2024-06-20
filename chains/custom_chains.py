from langchain_core.runnables import RunnableSequence
from langchain.prompts.prompt import PromptTemplate
from output_parsers import expertise_parser
from langchain_google_genai import GoogleGenerativeAI
import os

llm = GoogleGenerativeAI(model="gemini-pro")

def get_expertise_chain() -> RunnableSequence:
    """This chain is used to get the expertise of a person."""
    expertise_template = """given the information about a person from linkedin {information} I want you to get me his technical expertise of the person is he more suitable as Java developer or JavaScript developer
                            Answer should have two parts
                            part one is a string either Java or JavaScript or Do not know 
                            and part two interger of number of years of experience in the technology
                            \n{format_instructions}"""
    expertise_prompt_template = PromptTemplate(
        template=expertise_template, input_variables=["information"],partial_variables={
            "format_instructions": expertise_parser.get_format_instructions()
        },
    )
    return expertise_prompt_template | llm | expertise_parser