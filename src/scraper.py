import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_description(book_url):

    response = requests.get(book_url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    description_section = soup.select_one(
        "#product_description"
    )

    if description_section:

        description = (
            description_section
            .find_next_sibling("p")
            .get_text(strip=True)
        )

        return description

    return "No description available."


def scrape_category(category):

    category_url = (
        BASE_URL
        + "catalogue/category/books/"
        + category
        + "/index.html"
    )

    response = requests.get(category_url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    book_tags = soup.select(
        "article.product_pod"
    )

    books = []

    for book in book_tags:

        # -------------------------
        # TITLE
        # -------------------------

        title_tag = book.select_one("h3 a")

        title = title_tag["title"]


        # -------------------------
        # PRICE
        # -------------------------

        price_text = (
            book
            .select_one("p.price_color")
            .get_text(strip=True)
        )

        price = float(
            price_text.replace("£", "")
        )


        # -------------------------
        # RATING
        # -------------------------

        rating_tag = book.select_one(
            "p.star-rating"
        )

        rating_word = rating_tag["class"][1]

        rating = RATING_MAP[rating_word]


        # -------------------------
        # BOOK URL
        # -------------------------

        book_url = urljoin(
            category_url,
            title_tag["href"]
        )


        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "url": book_url
        })

    return books