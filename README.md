
# Bundesbank Document Scraper

## Introduction

This project implements a web scraper designed to download important documents from the Deutsche Bundesbank website. It targets documents within a specified date range and includes both English and German languages, focusing on speeches, interviews, and press releases.

## Project Structure

```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── constants.py
│   ├── document_parser.py
│   ├── scraper.py
│   └── utils.py
├── data
├── logs
├── main.py
├── requirements.txt
└── tests
    ├── __init__.py
    ├── test_document_parser.py
    ├── test_scraper.py
    └── test_utils.py
```

```
5 directories, 13 files
```

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the scraping process, simply run the `main.py` script. The script is currently configured to scrape documents for a predefined date range and specific document types.

The default settings are:

- Start Date: November 1, 2022
- End Date: December 31, 2022
- Document Types: Press-releases

You can modify these settings directly in the `main.py` file if needed. To do so, change the `start_date`, `end_date`, and `document_types` variables accordingly.

To run the script, use the following command:

```bash
python main.py
```

## Features

- **Robust Scraping**: Implements best practices such as rate limiting, exponential backoff, and request headers to mimic browser requests.
- **Logging**: Detailed logging of all operations, including successes and errors, saved in the `logs` directory.
- **In-Memory Processing**: Efficient processing of documents without the need for intermediate file storage.
- **Error Handling**: Graceful handling of errors, including retries and logging of errors.

## Modules

- `document_parser.py`: Parses HTML documents and extracts relevant details.
- `scraper.py`: Core scraping functionality, handling URL retrieval and document processing.
- `utils.py`: Utility functions including logging setup and request handling.
- `constants.py`: Configuration constants like request headers and URL patterns.

## Testing

To ensure the integrity and functionality of the components, automated tests have been written for various modules of the project. These tests are located in the `tests` directory.

To run these tests, simply execute the following command in your terminal:

```bash
pytest
```

## Output

The script outputs a JSON file in the `data` directory with the following structure:

```json
{
  "metadata": {
    "query_start_date": "YYYY-MM-DD",
    "query_end_date": "YYYY-MM-DD",
    "run_start_datetime": "YYYY-MM-DDTHH:MM:SSZ"
  },
  "errors": [...],
  "successes": [...]
}
```

## Contributing

Contributions to the project are welcome. Please follow standard coding conventions and add tests for new features.
