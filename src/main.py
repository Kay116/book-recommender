from categories import CATEGORIES
from scraper import scrape_category, get_description


def show_categories():

    print("\nChoose a category:\n")

    for number, info in CATEGORIES.items():

        print(
            f"{number}. {info['name']}"
        )


def main():

    print("=" * 60)
    print("📚 BOOK RECOMMENDER")
    print("=" * 60)

    show_categories()

    choice = input(
        "\nEnter category number: "
    ).strip()


    # -------------------------
    # CHECK CATEGORY
    # -------------------------

    if choice not in CATEGORIES:

        print("❌ Invalid category.")
        return


    selected = CATEGORIES[choice]

    print(
        f"\n📚 Category: {selected['name']}"
    )


    # -------------------------
    # USER PREFERENCES
    # -------------------------

    min_rating = int(
        input("⭐ Minimum rating (1-5): ")
    )

    max_price = float(
        input("💰 Maximum price: £")
    )


    # -------------------------
    # SCRAPE
    # -------------------------

    all_books = []

    print("\n🔎 Searching for books...")


    for category in selected["categories"]:

        books = scrape_category(category)

        all_books.extend(books)


    # -------------------------
    # FILTER
    # -------------------------

    results = []

    for book in all_books:

        if (
            book["rating"] >= min_rating
            and book["price"] <= max_price
        ):

            results.append(book)


    # -------------------------
    # SORT
    # -------------------------

    results.sort(
        key=lambda book: (
            -book["rating"],
            book["price"]
        )
    )


    # -------------------------
    # TOP 5
    # -------------------------

    top_5 = results[:5]


    print("\n" + "=" * 60)
    print("📚 YOUR TOP BOOK RECOMMENDATIONS")
    print("=" * 60)


    if len(top_5) == 0:

        print(
            "\n😕 No books match your preferences."
        )

        return


    # -------------------------
    # DESCRIPTION + OUTPUT
    # -------------------------

    for number, book in enumerate(
        top_5,
        start=1
    ):

        description = get_description(
            book["url"]
        )

        stars = "⭐" * book["rating"]

        print(
            f"\n{number}. {book['title']}"
        )

        print(
            f"   {stars} "
            f"({book['rating']}/5)"
        )

        print(
            f"   💰 £{book['price']:.2f}"
        )

        print(
            f"\n   📖 {description}"
        )

        print("\n" + "-" * 60)


if __name__ == "__main__":
    main() 