from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """
    Searches for the Linkedin or Twitter profile page of a person.

    Args:
        name (str): The name of the person to search for.

    Returns:
        str: The URL of the person's profile page.

    """
    print('this is the name', name)  # Print the name for debugging purposes

    # Create an instance of TavilySearchResults
    search = TavilySearchResults()

    # Run the search using the provided name
    res = search.run(f"{name}")

    # Return the URL of the first search result
    return res[0]["url"]