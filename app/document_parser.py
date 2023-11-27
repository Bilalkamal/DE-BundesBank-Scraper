# document_parser.py

from bs4 import BeautifulSoup
from datetime import datetime


class DocumentParser:
    """
    A class for parsing HTML documents and extracting document details.
    """

    def __init__(self, html_content):
        """
        Initialize the DocumentParser object.

        Args:
            html_content (str): The HTML content of the document.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.html_content = html_content

    def _extract_element_text(self, element, class_name):
        """
        Extract the text from an element with a specific class.

        Args:
            element (BeautifulSoup): The element to extract text from.
            class_name (str): The class of the element.

        Returns:
            str: The extracted text.
        """
        found_element = element.find(class_=class_name)
        return found_element.get_text(strip=True) if found_element else ''

    def extract_document_details(self, url):
        """
        Extract the document details from the HTML content.

        Args:
            url (str): The URL of the document.

        Returns:
            dict: A dictionary containing the document details.
        """
        main_content = self.soup.find('div', id='main-content')
        main = main_content.find('main', class_='main') if main_content else None

        document_text = self._extract_element_text(main, 'main') if main else ''
        document_title = self._extract_element_text(main, 'main__headline') if main else ''
        document_author = self._extract_element_text(main, 'metadata__authors') if main else ''

        return {
            "datetime_accessed": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "document_html": self.html_content,
            "document_text": document_text,
            "document_title": document_title,
            "document_html_source_language": "", 
            "document_text_source_language": "", 
            "document_title_source_language": "",
            "document_author": document_author,
            "document_url": url
        }