from bs4 import BeautifulSoup


def parse_book(html: str, url: str) -> dict:
    """
    Parse book information from an HTML page.

    Args:
        html: Raw HTML content of the book page.
        url: Source URL of the book.

    Returns:
        Dictionary containing the book title, description,
        rating, and source URL.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    # Extract description
    description_tag = soup.select_one("#product_description ~ p")
    description = (
        description_tag.get_text(" ", strip=True)
        if description_tag
        else ""
    )

    # Extract rating
    rating_tag = soup.select_one(".star-rating")
    rating = "Unknown"

    if rating_tag:
        rating_classes = rating_tag.get("class", [])

        if len(rating_classes) > 1:
            rating = rating_classes[1]

    return {
        "title": title,
        "description": description,
        "rating": rating,
        "url": url,
    }
