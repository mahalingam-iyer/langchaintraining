from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    print('this is the name', name)
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]