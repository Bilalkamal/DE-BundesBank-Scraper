# main.py

from datetime import date
from app.scraper import BundesbankScraper
from app.utils import setup_logging, write_json_to_disk

def main():
    """
    Main function for scraping and processing documents from Bundesbank.

    Returns:
        results (list): List of scraped and parsed documents.
    """
    # Set up logging
    setup_logging()

    # Define the date range and document types for scraping
    start_date = date.fromisoformat('2022-01-01')  # Start date of documents
    end_date = date.fromisoformat('2022-12-31')    # End date of documents
    document_types = ["Speeches", "Press-releases"]  # Options: "Speeches", "Interviews", "Press-releases"

    # Create an instance of BundesbankScraper
    scraper = BundesbankScraper(start_date, end_date, document_types)

    # Scrape and parse the documents
    results = scraper.scrape_documents()

    print(f"Number of documents scraped: {len(results['successes'])}")
    print(f"Number of documents failed: {len(results['errors'])}")

    # Write the results to disk
    query_details = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "run_date": date.today().strftime("%Y-%m-%d")
    }
    write_json_to_disk(results, query_details)

    return results



if __name__ == "__main__":
    main()
