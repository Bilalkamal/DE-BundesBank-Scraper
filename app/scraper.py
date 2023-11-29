# scraper.py

from typing import List, Dict
import os
import datetime
from datetime import datetime
import csv
import json
import requests
from datetime import date
from datetime import timedelta


from bs4 import BeautifulSoup
import logging



from utils import setup_logging, make_request_with_backoff
from document_parser import DocumentParser
from constants import HEADERS, BASE_URL, CONTENT_TYPE_PATHS, LANGUAGES, REFERER_BASE


class BundesbankScraper:
    """
    A class for scraping data from the Bundesbank website.
    """

    def __init__(self, start_date, end_date, content_types):
        """
        Initialize the BundesbankScraper object.

        Args:
            start_date (datetime): The start date for the data query.
            end_date (datetime): The end date for the data query.
            content_types (list): A list of content types to scrape.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.content_types = content_types
        self.all_urls = {lang: {ct: [] for ct in content_types} for lang in LANGUAGES}
        self.get_content_urls()

    def get_content_urls(self):
        """
        Retrieve the content URLs for the specified date range and content types.
        """
        date_from = self.start_date.strftime("%d.%m.%Y")
        date_to = self.end_date.strftime("%d.%m.%Y")

        for lang in LANGUAGES:
            logging.info(f"Retrieving content for {lang}...")
            for content_type in self.content_types:
                logging.info(f"Retrieving {content_type}...")
                self._get_content_urls_for_language(lang, content_type, date_from, date_to)

    def _get_content_urls_for_language(self, lang, content_type, date_from, date_to):
        """
        Retrieve the content URLs for a specific language and content type.

        Args:
            lang (str): The language.
            content_type (str): The content type.
            date_from (str): The start date in the format "dd.mm.yyyy".
            date_to (str): The end date in the format "dd.mm.yyyy".
        """
        page_num = 0
        while True:
            content_path = CONTENT_TYPE_PATHS[lang][content_type]
            HEADERS["Referer"] = REFERER_BASE[lang][content_type]
            page_url = f"{BASE_URL}/action/{'en' if lang == 'English' else 'de'}/{content_path}/bbksearch?query=&tfi-730578=&tfi-730576=&dateFrom={date_from}&dateTo={date_to}&hitsPerPageString=50&sort=bbksortdate+desc&pageNumString={page_num}"
            response = make_request_with_backoff(page_url)
            print(page_url)
            if not response:
                break
            soup = BeautifulSoup(response.content, "html.parser")

            ul = soup.find('ul', class_='resultlist')
            if not ul:
                break
            links = ul.find_all('a', class_='teasable__link')
            urls = [link['href'] if link['href'].startswith('https') else f"{BASE_URL}{link['href']}" for link in links if 'href' in link.attrs]
            logging.info(f"Found {len(urls)} links on page {page_num + 1}.")
            if len(urls) < 50 or set(urls).issubset(set(self.all_urls[lang][content_type])):
                self.all_urls[lang][content_type].extend(urls)
                break
            self.all_urls[lang][content_type].extend(urls)
            page_num += 1

    def scrape_documents(self):
        """
        Scrape the documents from the retrieved content URLs.

        Returns:
            dict: A dictionary containing the scraped document details.
        """
        results = {
            "metadata": {
                "query_start_date": self.start_date.isoformat(),
                "query_end_date": self.end_date.isoformat(),
                "run_start_datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "errors": [],
            "successes": []
        }
        
        for language, content in self.all_urls.items():
            for content_type, urls in content.items():
                logging.info(f"Downloading {content_type} in {language}...")
                self._scrape_documents_for_language(language, content_type, urls, results)
        
        return results

    def _scrape_documents_for_language(self, language, content_type, urls, results):
        """
        Scrape the documents for a specific language and content type.

        Args:
            language (str): The language.
            content_type (str): The content type.
            urls (list): A list of URLs to scrape.
            results (dict): The dictionary to store the scraped document details.
        """
        for url in urls:
            response = make_request_with_backoff(url)
            if response:
                parser = DocumentParser(response.text)
                details = parser.extract_document_details(url)
                results["successes"].append(details)
            else:
                results["errors"].append(url)

    

def get_countries() -> List[Dict[str, str]]:
    """
    Return a list of countries obtained from a RestAPI via the requests library.

    :return: A list of dictionaries with the keys (name, region, iso2, scrape_datetime).
    """ 
    response = requests.get('https://restcountries.com/v3.1/all', verify=False).json()
    
    return [{
        'name': record.get('name').get('official'),
        'region': record.get('region'),
        'iso2': record.get('cca2'),
        'scrape_datetime': datetime.datetime.utcnow().strftime('%Y-%m-%s')
    } for record in response]


def run(filename: str):
    """
    This function will be the main entrypoint to your code and will be called with a filename.
    """
    
    # countries = get_countries()
    setup_logging()
    today = date.today()
    start_date = today + timedelta(days=-2)
    print(start_date)
    end_date = today + timedelta(days=1)
    print(end_date)

    # # Define the date range and document types for scraping
    # start_date = date.fromisoformat('2023-11-26')  # Start date of documents
    # end_date = date.fromisoformat('2023-11-29')    # End date of documents
    document_types = [ "Press-releases"]  # Options: "Speeches", "Interviews", "Press-releases"

    # Create an instance of BundesbankScraper
    results = BundesbankScraper(start_date, end_date, document_types).scrape_documents()

    # Scrape and parse the documents
    json.dump(results, open(filename, 'w'))    


if __name__ == "__main__":
    run('data.json')