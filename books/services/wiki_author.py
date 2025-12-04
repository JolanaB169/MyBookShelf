"""
Service to fetch author bio from Wikipedia.
"""

import wikipediaapi

def get_author_bio(author_name, lang="en"):
    """
    Fetch a short biography of the author from Wikipedia.

    Args:
        author_name (str): Full name of the author.
        lang (str): Wikipedia language code, default 'en'.

    Returns:
        str: Short biography text or empty string if not found.
    """
    wiki = wikipediaapi.Wikipedia(
        language=lang,
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="MyBookShelfApp/1.0"
    )
    page = wiki.page(author_name)
    if page.exists():
        # Return the first paragraph
        bio = page.summary.split("\n")[0]
        return bio
    return ""