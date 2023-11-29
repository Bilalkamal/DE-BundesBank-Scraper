from app.document_parser import DocumentParser
from bs4 import BeautifulSoup
import pytest
from datetime import datetime

# Sample HTML content for testing
SAMPLE_HTML = """
<html>
    <body>
        <div id='main-content'>
            <main class='main'>
                <h1 class='main__headline'>Test Title</h1>
                <p class='metadata__authors'>Test Author</p>
                <div class='main'>Test Document Text</div>
            </main>
        </div>
    </body>
</html>
"""

# Test URL for the document
TEST_URL = "http://example.com/test_document"

@pytest.fixture
def parser():
    """Fixture to create a DocumentParser object with sample HTML."""
    return DocumentParser(SAMPLE_HTML)

def test_extract_element_text(parser):
    """Test the _extract_element_text method of DocumentParser."""
    soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
    main_content = soup.find('div', id='main-content')
    main = main_content.find('main', class_='main') if main_content else None

    assert parser._extract_element_text(main, 'main__headline') == 'Test Title'
    assert parser._extract_element_text(main, 'metadata__authors') == 'Test Author'
    assert parser._extract_element_text(main, 'nonexistent_class') == ''

def test_extract_document_details(parser):
    """Test the extract_document_details method of DocumentParser."""
    details = parser.extract_document_details(TEST_URL)

    assert details['document_url'] == TEST_URL
    assert details['document_html'] == SAMPLE_HTML
    assert details['document_title'] == 'Test Title'
    assert details['document_text'] == 'Test Document Text'
    assert details['document_author'] == 'Test Author'
    assert datetime.strptime(details['datetime_accessed'], "%Y-%m-%dT%H:%M:%SZ")
