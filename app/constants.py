# Constants.py

# Time in seconds between requests
REQUEST_DELAY = 10

# Maximum backoff time in seconds (5 minutes)
MAX_BACKOFF_TIME = 300



# Headers for HTTP requests
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Dnt": "1",
    "Host": "www.bundesbank.de",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
}


# Base URL for requests
BASE_URL = "https://www.bundesbank.de"

# Languages supported
LANGUAGES = ["English", "German"]

# Paths for different content types in each language
CONTENT_TYPE_PATHS = {
    "English": {
        "Speeches": "730564",
        "Interviews": "730132",
        "Press-releases": "730186"
    },
    "German": {
        "Speeches": "729950",
        "Interviews": "729904",
        "Press-releases": "724000"
    }
}

# Referer base URLs for different content types in each language
REFERER_BASE = {
    "English": {
        "Speeches": "https://www.bundesbank.de/en/press/speeches",
        "Interviews": "https://www.bundesbank.de/en/press/interviews",
        "Press-releases": "https://www.bundesbank.de/en/press/press-releases"
    },
    "German": {
        "Speeches": "https://www.bundesbank.de/de/presse/reden",
        "Interviews": "https://www.bundesbank.de/de/presse/interviews",
        "Press-releases": "https://www.bundesbank.de/de/presse/pressenotizen"
    }
}