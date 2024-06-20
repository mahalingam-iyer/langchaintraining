from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import os
from langchain.prompts.prompt import PromptTemplate
from tools.tools import get_profile_url_tavily
from langchain_core.tools import Tool
from langchain import hub

from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)

# Load environment variables from .env file
load_dotenv()

def lookup(name: str) -> str:
    # Initialize the GoogleGenerativeAI model
    llm = GoogleGenerativeAI(model="gemini-pro")
    
    # Define the template for the prompt
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""
    
    # Create a PromptTemplate object with the template and input variables
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    
    # Define a list of tools for the agent
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]
    
    # Pull the react prompt from the hub
    react_prompt = hub.pull("hwchase17/react")
    
    # Create a react agent using the GoogleGenerativeAI model, tools, and prompt
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    
    # Create an AgentExecutor object with the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    # Invoke the agent with the input prompt generated from the template and name parameter
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    
    # Extract the linkedin profile URL from the agent's output
    linked_profile_url = result["output"]
    
    # Return the linkedin profile URL
    return linked_profile_url
