import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("proxy_curl_api")}'}
    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url},
        headers=header_dic,
        timeout=10,
    )
    data = response.json()
    return data