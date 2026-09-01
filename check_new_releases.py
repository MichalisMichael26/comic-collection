# ============================================================
# CHECK NEW COMIC RELEASES
#
# Ελέγχει τη Μαμούθ για νέα αριθμημένα τεύχη.
#
# Δημιουργεί:
# static/new_releases.json
# ============================================================

from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin

import json
import re
import unicodedata

import requests
from bs4 import BeautifulSoup


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"

OUTPUT_FILE = (
    STATIC_DIR
    / "new_releases.json"
)


# ============================================================
# SOURCE
# ============================================================

MAMOUTH_COMICS_URL = (
    "https://mamouthcomix-eshop.gr/"
    "product-category/"
    "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
)


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),

    "Accept-Language":
        "el-GR,el;q=0.9,en;q=0.8"

}


# ============================================================
# ΤΙ ΕΧΟΥΜΕ ΗΔΗ ΣΤΟ APP
# ============================================================

KNOWN_MAX = {

    "lucky-luke": 90,

    "asterix": 41,

    "idefix": 2,

    "iznogoud": 30,

    "rantanplan": 17,

    "sherlock-holmes": 4

}


SERIES_NAMES = {

    "lucky-luke":
        "Λούκυ Λουκ",

    "asterix":
        "Αστερίξ",

    "idefix":
        "Ιντεφίξ",

    "iznogoud":
        "Ιζνογκούντ",

    "rantanplan":
        "Ραντανπλάν",

    "sherlock-holmes":
        "Σέρλοκ Χολμς"

}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text):

    text = str(text)

    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        character
        for character in text
        if unicodedata.category(character)
        != "Mn"
    )

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SERIES + NUMBER
# ============================================================

def identify_comic(title):

    normalized = normalize_text(
        title
    )


    # --------------------------------------------------------
    # Δεν θέλουμε σκληρόδετα / special editions
    # --------------------------------------------------------

    forbidden = [

        "σκληροδετο",

        "πολυτελης",

        "πολυτελη"

    ]


    for word in forbidden:

        if word in normalized:

            return None


    # --------------------------------------------------------
    # LUCKY LUKE
    # --------------------------------------------------------

    match = re.search(
        r"λουκυ\s+λουκ\s*0?(\d{1,3})",
        normalized
    )


    if match:

        return (
            "lucky-luke",
            int(match.group(1))
        )


    # --------------------------------------------------------
    # ASTERIX
    # --------------------------------------------------------

    match = re.search(
        r"αστεριξ\s*0?(\d{1,3})",
        normalized
    )


    if match:

        return (
            "asterix",
            int(match.group(1))
        )


    # --------------------------------------------------------
    # IDEFIX
    #
    # π.χ.
    # Ο Ιντεφίξ και οι Ανυπότακτοι # 02
    # --------------------------------------------------------

    if "ιντεφιξ" in normalized:

        match = re.search(
            r"#\s*0?(\d{1,3})",
            normalized
        )


        if match:

            return (
                "idefix",
                int(match.group(1))
            )


    # --------------------------------------------------------
    # IZNOGOUD
    # --------------------------------------------------------

    match = re.search(
        r"ιζνογκουντ\s*0?(\d{1,3})",
        normalized
    )


    if match:

        return (
            "iznogoud",
            int(match.group(1))
        )


    # --------------------------------------------------------
    # RANTANPLAN
    # --------------------------------------------------------

    match = re.search(
        r"ραντανπλαν\s*0?(\d{1,3})",
        normalized
    )


    if match:

        return (
            "rantanplan",
            int(match.group(1))
        )


    # --------------------------------------------------------
    # SHERLOCK HOLMES
    # --------------------------------------------------------

    match = re.search(
        r"σερλοκ\s+χολμς\s*0?(\d{1,3})",
        normalized
    )


    if match:

        return (
            "sherlock-holmes",
            int(match.group(1))
        )


    return None


# ============================================================
# PRODUCT IMAGE
# ============================================================

def get_product_image(
    product,
    page_url
):

    image = product.select_one(
        "img"
    )


    if not image:

        return ""


    possible = [

        image.get(
            "data-large_image"
        ),

        image.get(
            "data-lazy-src"
        ),

        image.get(
            "data-src"
        ),

        image.get(
            "src"
        )

    ]


    for value in possible:

        if (
            value
            and
            not value.startswith("data:")
        ):

            return urljoin(
                page_url,
                value
            )


    return ""


# ============================================================
# PRODUCT DATA
# ============================================================

def parse_product(
    product,
    page_url
):

    title_element = (

        product.select_one(
            ".woocommerce-loop-product__title"
        )

        or product.select_one(
            "h2"
        )

        or product.select_one(
            "h3"
        )

    )


    if not title_element:

        return None


    title = title_element.get_text(
        " ",
        strip=True
    )


    comic = identify_comic(
        title
    )


    if not comic:

        return None


    series, number = comic


    link_element = (

        product.select_one(
            "a.woocommerce-LoopProduct-link"
        )

        or product.select_one(
            "a.woocommerce-loop-product__link"
        )

        or product.select_one(
            'a[href*="/product/"]'
        )

        or product.find(
            "a"
        )

    )


    product_url = ""


    if (
        link_element
        and
        link_element.get("href")
    ):

        product_url = urljoin(
            page_url,
            link_element.get("href")
        )


    image_url = get_product_image(
        product,
        page_url
    )


    return {

        "series":
            series,

        "series_name":
            SERIES_NAMES.get(
                series,
                series
            ),

        "number":
            number,

        "title":
            title,

        "product_url":
            product_url,

        "image_url":
            image_url

    }


# ============================================================
# SCAN MAMOUTH
# ============================================================

def scan_mamouth():

    found = []


    # Αυτή τη στιγμή η κατηγορία κόμιξ
    # έχει αρκετές σελίδες.
    # Βάζουμε μέχρι 15 για μελλοντική επέκταση.

    for page in range(
        1,
        16
    ):


        if page == 1:

            page_url = (
                MAMOUTH_COMICS_URL
            )


        else:

            page_url = (
                MAMOUTH_COMICS_URL
                +
                f"page/{page}/"
            )


        print(
            f"Checking page {page}..."
        )


        try:

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=20
            )


        except Exception as error:

            print(
                f"Request failed: {error}"
            )

            continue


        # Αν φτάσουμε μετά την τελευταία
        # πραγματική σελίδα σταματάμε.

        if response.status_code == 404:

            break


        if response.status_code != 200:

            continue


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        products = soup.select(
            "li.product"
        )


        if not products:

            # Μπορεί να αλλάξει το template,
            # δεν θεωρούμε απαραίτητα ότι είναι error.

            continue


        for product in products:

            item = parse_product(
                product,
                page_url
            )


            if item:

                found.append(
                    item
                )


    return found


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def deduplicate(items):

    unique = {}


    for item in items:

        key = (
            item["series"],
            item["number"]
        )


        # Κρατάμε την πρώτη κανονική έκδοση
        # που βρήκαμε.

        if key not in unique:

            unique[key] = item


    return list(
        unique.values()
    )


# ============================================================
# BUILD REPORT
# ============================================================

def build_report(
    products
):

    latest_detected = {

        series:
            0

        for series
        in KNOWN_MAX
    }


    new_releases = []


    for item in products:

        series = item["series"]

        number = item["number"]


        if series not in KNOWN_MAX:

            continue


        if (
            number
            >
            latest_detected[series]
        ):

            latest_detected[
                series
            ] = number


        if (
            number
            >
            KNOWN_MAX[series]
        ):

            new_releases.append(
                item
            )


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    new_releases.sort(
        key=lambda item: (
            item["series"],
            item["number"]
        )
    )


    return {

        "checked_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "source":
            MAMOUTH_COMICS_URL,

        "known_max":
            KNOWN_MAX,

        "latest_detected":
            latest_detected,

        "new_releases":
            new_releases,

        "new_count":
            len(new_releases)

    }


# ============================================================
# MAIN
# ============================================================

def main():

    STATIC_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    print()
    print(
        "=========================================="
    )
    print(
        "CHECKING FOR NEW COMIC RELEASES"
    )
    print(
        "=========================================="
    )
    print()


    products = scan_mamouth()


    products = deduplicate(
        products
    )


    report = build_report(
        products
    )


    OUTPUT_FILE.write_text(

        json.dumps(
            report,
            ensure_ascii=False,
            indent=4
        ),

        encoding="utf-8"

    )


    print()
    print(
        "=========================================="
    )
    print(
        "RESULT"
    )
    print(
        "=========================================="
    )


    for series, known in KNOWN_MAX.items():

        detected = (
            report[
                "latest_detected"
            ].get(
                series,
                0
            )
        )


        print(
            f"{SERIES_NAMES[series]}: "
            f"App #{known} | "
            f"Detected #{detected}"
        )


    print()


    if report[
        "new_releases"
    ]:

        print(
            "🆕 NEW RELEASES FOUND:"
        )


        for item in report[
            "new_releases"
        ]:

            print(
                f"🆕 "
                f"{item['series_name']} "
                f"#{item['number']} - "
                f"{item['title']}"
            )


    else:

        print(
            "✅ Δεν βρέθηκαν νέα αριθμημένα τεύχη."
        )


    print()
    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()
