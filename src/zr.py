import requests
from bs4 import BeautifulSoup
import json

def get_zr_data(url: str) -> dict:
    """
    Extracts a set of data from a zwiftracing url and writes it to an json object
    """
    # Send a GET request to the URL
    response = requests.get(url, verify=False)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the __NEXT_DATA__ JSON string
    next_data_script = soup.find("script", id="__NEXT_DATA__")
    if not next_data_script:
        raise ValueError("Could not find __NEXT_DATA__ script tag on the page.")

    next_data_json = json.loads(next_data_script.string)["props"]["pageProps"]
    return next_data_json

def find_velo_score(url:str) -> dict:
    all_data = get_zr_data(url)
    velo = {}
    overall = all_data['rider']['race']['rating']
    velo['overall'] = overall
    handicaps = all_data['rider']['handicaps']['profile']
    velo['flat'] = overall + handicaps['flat']
    velo['rolling'] = overall + handicaps['rolling']
    velo['hilly'] = overall + handicaps['hilly']
    velo['mountainous'] = overall + handicaps['mountainous']
    return velo

if __name__ == "__main__":
    print(find_velo_score('https://www.zwiftracing.app/riders/2882571'))