"""
utils.py - utility functions that will help in project.

random_ua(): Returns a random user agent string.
normalize_url(url): Normalize url by removing extra parameters from the url.
"""

import random
from constants import USER_AGENTS
from urllib.parse import urljoin, urlparse


def random_ua() -> str:
    """
    Returns a random user agent string.

    Returns:
        str: A random user agent.
    """

    return random.choice(USER_AGENTS)


def normalize_url(url: str) -> str:
    """
    Normalize the url by removing extra parameters from the url such search params etc.

    Args:
        url (str): The raw url scrapped form the page.

    Returns:
        str: Normalized URL.


    """

    path = urlparse(url).path
    normalized_url = urljoin(url, path)

    return str(normalized_url)
