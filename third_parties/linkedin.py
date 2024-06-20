import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles.

    This function manually scrapes information from a LinkedIn profile using a third-party API.

    Args:
        linkedin_profile_url (str): The URL of the LinkedIn profile to scrape.
        mock (bool, optional): Whether to use mock data for testing purposes. Defaults to False.

    Returns:
        dict: A dictionary containing the scraped data from the LinkedIn profile.
    """

    # API endpoint for the third-party service
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    # Set the authorization header with the API key from environment variables
    header_dic = {"Authorization": f'Bearer {os.environ.get("proxy_curl_api")}'}

    # Send a GET request to the API endpoint with the LinkedIn profile URL as a parameter
    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url},
        headers=header_dic,
        timeout=10,
    )

    # Parse the response as JSON
    data = response.json()

    # Return the scraped data
    return data