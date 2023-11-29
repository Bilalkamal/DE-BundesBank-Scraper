from datetime import datetime
import pytest
from unittest.mock import patch, MagicMock
from app.scraper import BundesbankScraper
from app.document_parser import DocumentParser

# Mock response for HTML content (as string)
mock_html_content = "<html><body><ul class='resultlist'><a class='teasable__link' href='https://example.com/document1'>Document 1</a></ul></body></html>"

# Update mock response for network request
mock_response = MagicMock()
mock_response.status_code = 200
mock_response.content = mock_html_content.encode('utf-8')  
mock_response.text = mock_html_content  


@patch('scraper.make_request_with_backoff', return_value=mock_response)
def test_get_content_urls(mock_request):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)
    content_types = ["Speeches"]

    scraper = BundesbankScraper(start_date, end_date, content_types)
    scraper.get_content_urls()

    # Assert that URLs have been added to all_urls
    for lang in scraper.all_urls:
        for content_type in scraper.all_urls[lang]:
            assert scraper.all_urls[lang][content_type] != []

@patch('scraper.make_request_with_backoff', return_value=mock_response)
def test_scrape_documents(mock_request):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)
    content_types = ["Speeches"]

    scraper = BundesbankScraper(start_date, end_date, content_types)
    scraper.get_content_urls()  # Populate all_urls with mock data
    results = scraper.scrape_documents()

    # Assert that results contain successes and metadata
    assert 'successes' in results
    assert 'metadata' in results
    assert results['successes']


