# utils.py


from app.constants import HEADERS, MAX_BACKOFF_TIME

import requests
import logging
import time
import os
import json
from datetime import datetime


def setup_logging():
    """
    Sets up logging for the application.

    This function creates a log directory if it doesn't exist and sets up a log file with the current date as the filename.
    The log file will contain log messages with the format: "<timestamp> <log_level>: <message>".

    Args:
        None

    Returns:
        None
    """
    log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_directory, exist_ok=True)
    log_filename = os.path.join(log_directory, datetime.now().strftime("%Y-%m-%d-run.log"))
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='w')


def make_request_with_backoff(url, max_backoff=MAX_BACKOFF_TIME):
    """
    Makes a request to the specified URL with exponential backoff.

    Args:
        url (str): The URL to make the request to.
        max_backoff (int): The maximum backoff time in seconds (default: MAX_BACKOFF_TIME).

    Returns:
        requests.Response or None: The response object if the request is successful, None otherwise.
    """
    backoff_time = 1  # Initial backoff time in seconds
    while backoff_time <= max_backoff:
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                logging.info(f"Successfully downloaded URL: {url}")
                return response
            elif response.status_code == 429 or 500 <= response.status_code < 600:
                logging.error(f"Error {response.status_code} for URL: {url}. Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                backoff_time *= 2  # Exponential backoff
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception for URL: {url}. Error: {e}")
            if backoff_time >= max_backoff:
                logging.error(f"ERROR: Request failed after maximum backoff time for URL: {url}")
                return None
            else:
                time.sleep(backoff_time)
                backoff_time *= 2
    return None


def write_json_to_disk(json_object, query_details):
    """
    Writes a JSON object to disk.

    Args:
        json_object (dict): The JSON object to be written.
        query_details (dict): Details of the query used to generate the JSON object.

    Returns:
        None
    """
    data_directory = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_directory, exist_ok=True)
    filename = f"{query_details['start_date']}_{query_details['end_date']}_{query_details['run_date']}.json"
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'w') as f:
        json.dump(json_object, f)
    logging.info(f"Successfully wrote JSON to disk: {filename}")