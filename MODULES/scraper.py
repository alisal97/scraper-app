import requests
from bs4 import BeautifulSoup
import logging
import config

logging.basicConfig(filename='scraper.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def finder(homepage_url):
    try:
        response = requests.get(homepage_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        pages = config.page_keywords
        links = []

        for a_tag in soup.find_all('a', href=True):
            if any(keyword in a_tag.text.lower() or keyword in a_tag['href'].lower() for keyword in pages):
                link = a_tag['href']
                if not link.startswith('http'):
                    link = homepage_url.rstrip('/') + '/' + link.lstrip('/')
                links.append(link)

        return links if links else ["pages not found."]
    except requests.RequestException as e:
        logging.error(f"Error occurred {e}")
        return None
    
def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for nocon in soup(["script", "style", "img"]):
            nocon.decompose()

        text = soup.get_text()

        links = []
        for link in soup.find_all('a', href=True):
            links.append({'text': link.get_text(strip=True), 'url': link['href']})

        content = {'text': text, 'links': links}
        return content
    except requests.RequestException as e:
        logging.error(f"Error occurred {e}")
        return None
