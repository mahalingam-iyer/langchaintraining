from langchain import Tool, Agent

# Define a tool that stores and retrieves the user's name using LangChain Memory
def remember_name(memory, name):
    memory['user_name'] = name
    return f"Okay, I'll remember your name as {name}."

def greet_user(memory):
    if 'user_name' in memory:
        return f"Hello, {memory['user_name']}!"
    else:
        return "Hello! What's your name?"

# Define tools for the agent
tools_for_agent = [
    Tool(name="Remember Name", func=remember_name),
    Tool(name="Greet User", func=greet_user),
]

# Create an agent with the defined tools
agent = Agent(tools=tools_for_agent)
# Example interaction with the agent
print(agent.execute("Greet User"))
print(agent.execute("Remember Name", "Alice"))
print(agent.execute("Greet User"))
