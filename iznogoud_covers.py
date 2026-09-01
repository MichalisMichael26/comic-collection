# ============================================================
# IZNOGOUD COVER SERVICE
#
# Βρίσκει covers Ιζνογκούντ από την επίσημη
# κατηγορία της Μαμούθ.
#
# Δεν χρησιμοποιείται όταν ανοίγει το site.
# Χρησιμοποιείται μόνο από download_covers.py.
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin
import json
import re
import unicodedata

import requests
from bs4 import BeautifulSoup


# ============================================================
# SETTINGS
# ============================================================

BASE_URL = "https://mamouthcomix-eshop.gr/"


CATEGORY_URLS = [

    (
        "https://mamouthcomix-eshop.gr/"
        "product-category/"
        "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
        "%CE%B9%CE%B6%CE%BD%CE%BF%CE%B3%CE%BA%CE%BF%CF%8D%CE%BD%CF%84/"
    ),

    (
        "https://mamouthcomix-eshop.gr/"
        "en/product-category/"
        "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
        "%CE%B9%CE%B6%CE%BD%CE%BF%CE%B3%CE%BA%CE%BF%CF%8D%CE%BD%CF%84/"
    )

]


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),

    "Accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/xml;q=0.9,"
        "image/avif,"
        "image/webp,"
        "*/*;q=0.8"
    ),

    "Accept-Language":
        "el-GR,el;q=0.9,en;q=0.8",

    "Cache-Control":
        "no-cache"

}


# ============================================================
# TITLES
# ============================================================

IZNOGOUD_TITLES = {

    1: "Ο μεγάλος Βεζίρης Ιζνογκούντ",

    2: "Οι συνωμοσίες του μεγάλου Βεζίρη Ιζνογκούντ",

    3: "Οι διακοπές του Χαλίφη",

    4: "Αστράκια για τον Ιζνογκούντ",

    5: "Ιζνογκούντ ο απαίσιος",

    6: "Ο μαγικός υπολογιστής",

    7: "Ένα καρότο για τον Ιζνογκούντ",

    8: "Η μέρα των τρελών",

    9: "Το μαγικό χαλί",

    10: "Ο μαινόμενος",

    11: "Το κεφάλι του Τούρκου του Ιζνογκούντ",

    12: "Μια νεράιδα για τον Ιζνογκούντ",

    13: "Θέλω να γίνω Χαλίφης στη θέση του Χαλίφη",

    14: "Ο συνένοχος του Ιζνογκούντ",

    15: "Ο Ιζνογκούντ επιτέλους Χαλίφης",

    16: "Ο Ιζνογκούντ και οι γυναίκες",

    17: "Η επέτειος του Ιζνογκούντ",

    18: "Τα παιδικά χρόνια του Ιζνογκούντ",

    19: "Η παγίδα της σειρήνας",

    20: "Οι επιστροφές του Ιζνογκούντ",

    21: "Οι εφιάλτες του Ιζνογκούντ - Τόμος 1",

    22: "Οι εφιάλτες του Ιζνογκούντ - Τόμος 2",

    23: "Οι εφιάλτες του Ιζνογκούντ - Τόμος 3",

    24: "Οι εφιάλτες του Ιζνογκούντ - Τόμος 4",

    25: "Ποιος σκότωσε το Χαλίφη;",

    26: "Το συμπαθητικό τέρας",

    27: "Το λάθος του προγόνου",

    28: "Οι Χίλιες και Μία Νύχτες του Χαλίφη",

    29: "Ο Ιζνογκούντ Πρόεδρος",

    30: "Από Πατέρα σε Γιο"

}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text):

    if not text:
        return ""

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

    text = text.replace(
        "ς",
        "σ"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# ISSUE NUMBER
# ============================================================

def extract_number(text):

    text = normalize_text(
        text
    )


    if "ιζνογκουντ" not in text:

        return None


    patterns = [

        r"ιζνογκουντ\s*#?\s*0?(\d{1,2})",

        r"ιζνογκουντ\s*[-–—:]\s*0?(\d{1,2})",

        r"ιζνογκουντ.*?0?(\d{1,2})"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )


        if not match:

            continue


        try:

            number = int(
                match.group(1)
            )

        except Exception:

            continue


        if 1 <= number <= 30:

            return number


    return None


# ============================================================
# CLEAN URL
# ============================================================

def clean_url(
    url,
    base_url=BASE_URL
):

    if not url:

        return None


    url = str(
        url
    ).strip()


    if not url:

        return None


    if url.startswith(
        "data:"
    ):

        return None


    return urljoin(
        base_url,
        url
    )


# ============================================================
# GET IMAGE FROM IMG
# ============================================================

def image_from_tag(
    image,
    base_url
):

    if not image:

        return None


    attributes = [

        "data-large_image",

        "data-lazy-src",

        "data-src",

        "data-original",

        "src"

    ]


    for attribute in attributes:

        value = image.get(
            attribute
        )


        value = clean_url(
            value,
            base_url
        )


        if value:

            return value


    # ========================================================
    # SRCSET
    # ========================================================

    srcset = image.get(
        "srcset"
    )


    if srcset:

        entries = (
            srcset.split(",")
        )


        for entry in reversed(
            entries
        ):

            candidate = (
                entry
                .strip()
                .split(" ")[0]
            )


            candidate = clean_url(
                candidate,
                base_url
            )


            if candidate:

                return candidate


    return None


# ============================================================
# PRODUCT PAGE IMAGE
# ============================================================

def get_product_page_image(
    product_url
):

    if not product_url:

        return None


    try:

        response = requests.get(

            product_url,

            headers=HEADERS,

            timeout=25,

            allow_redirects=True

        )


    except Exception:

        return None


    if response.status_code != 200:

        return None


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # ========================================================
    # OG IMAGE
    # ========================================================

    meta_selectors = [

        'meta[property="og:image"]',

        'meta[property="og:image:secure_url"]',

        'meta[name="twitter:image"]',

        'meta[property="twitter:image"]'

    ]


    for selector in meta_selectors:

        meta = soup.select_one(
            selector
        )


        if not meta:

            continue


        image_url = clean_url(
            meta.get("content"),
            response.url
        )


        if image_url:

            return image_url


    # ========================================================
    # WOOCOMMERCE IMAGE
    # ========================================================

    selectors = [

        ".woocommerce-product-gallery__image img",

        ".woocommerce-product-gallery img",

        "img.wp-post-image",

        ".product-images img",

        ".product-image img"

    ]


    for selector in selectors:

        image = soup.select_one(
            selector
        )


        image_url = image_from_tag(
            image,
            response.url
        )


        if image_url:

            return image_url


    # ========================================================
    # JSON-LD
    # ========================================================

    scripts = soup.select(
        'script[type="application/ld+json"]'
    )


    for script in scripts:

        try:

            data = json.loads(
                script.string
                or
                script.get_text()
            )


        except Exception:

            continue


        objects = []


        if isinstance(
            data,
            list
        ):

            objects.extend(
                data
            )


        elif isinstance(
            data,
            dict
        ):

            objects.append(
                data
            )


            graph = data.get(
                "@graph"
            )


            if isinstance(
                graph,
                list
            ):

                objects.extend(
                    graph
                )


        for item in objects:

            if not isinstance(
                item,
                dict
            ):

                continue


            image = item.get(
                "image"
            )


            if isinstance(
                image,
                str
            ):

                image_url = clean_url(
                    image,
                    response.url
                )


                if image_url:

                    return image_url


            if isinstance(
                image,
                list
            ):

                for value in image:

                    if isinstance(
                        value,
                        str
                    ):

                        image_url = clean_url(
                            value,
                            response.url
                        )


                        if image_url:

                            return image_url


    return None


# ============================================================
# PARSE CATEGORY
# ============================================================

def parse_category_page(
    url
):

    results = {}


    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=25,

            allow_redirects=True

        )


    except Exception:

        return results


    if response.status_code != 200:

        return results


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # ========================================================
    # ΜΕΘΟΔΟΣ 1:
    # PRODUCT CARDS
    # ========================================================

    cards = soup.select(
        "li.product"
    )


    for card in cards:

        card_text = card.get_text(
            " ",
            strip=True
        )


        number = extract_number(
            card_text
        )


        if number is None:

            continue


        product_link = (

            card.select_one(
                'a[href*="/product/"]'
            )

            or card.find(
                "a",
                href=True
            )

        )


        product_url = None


        if product_link:

            product_url = clean_url(
                product_link.get(
                    "href"
                ),
                response.url
            )


        # ====================================================
        # ΠΡΩΤΑ ΠΡΟΣΠΑΘΟΥΜΕ ΑΠΟ ΤΟ CARD
        # ====================================================

        card_image = image_from_tag(

            card.find(
                "img"
            ),

            response.url

        )


        results[number] = {

            "product_url":
                product_url,

            "card_image":
                card_image

        }


    # ========================================================
    # ΜΕΘΟΔΟΣ 2:
    # ΟΛΑ ΤΑ LINKS
    #
    # Αυτό είναι fallback αν αλλάξει το WooCommerce template.
    # ========================================================

    anchors = soup.find_all(
        "a",
        href=True
    )


    for anchor in anchors:

        href = anchor.get(
            "href",
            ""
        )


        if "/product/" not in href:

            continue


        text = anchor.get_text(
            " ",
            strip=True
        )


        number = extract_number(
            text
        )


        if number is None:

            title_attribute = (
                anchor.get("title")
                or
                anchor.get("aria-label")
                or
                ""
            )


            number = extract_number(
                title_attribute
            )


        if number is None:

            continue


        product_url = clean_url(
            href,
            response.url
        )


        if number not in results:

            results[number] = {

                "product_url":
                    product_url,

                "card_image":
                    None

            }


        elif not results[
            number
        ].get(
            "product_url"
        ):

            results[
                number
            ][
                "product_url"
            ] = product_url


    return results


# ============================================================
# SEARCH FALLBACK
# ============================================================

def search_product(
    number
):

    search_terms = [

        f"Ιζνογκούντ {number:02d}",

        f"Ιζνογκούντ {number}",

        (
            f"Ιζνογκούντ "
            f"{IZNOGOUD_TITLES[number]}"
        )

    ]


    for search_term in search_terms:

        try:

            response = requests.get(

                BASE_URL,

                params={
                    "s":
                        search_term,

                    "post_type":
                        "product"
                },

                headers=HEADERS,

                timeout=20,

                allow_redirects=True

            )


        except Exception:

            continue


        if response.status_code != 200:

            continue


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        anchors = soup.find_all(
            "a",
            href=True
        )


        for anchor in anchors:

            href = anchor.get(
                "href",
                ""
            )


            if "/product/" not in href:

                continue


            text = anchor.get_text(
                " ",
                strip=True
            )


            detected = extract_number(
                text
            )


            if detected != number:

                continue


            product_url = clean_url(
                href,
                response.url
            )


            image_url = get_product_page_image(
                product_url
            )


            if image_url:

                return image_url


    return None


# ============================================================
# BUILD CATALOG
# ============================================================

@lru_cache(maxsize=1)
def build_catalog():

    catalog = {}


    product_data = {}


    # ========================================================
    # DIRECT IZNOGOUD CATEGORY
    # ========================================================

    for category_url in CATEGORY_URLS:

        found = parse_category_page(
            category_url
        )


        for number, data in found.items():

            if number not in product_data:

                product_data[
                    number
                ] = data


            else:

                if (
                    not product_data[
                        number
                    ].get(
                        "product_url"
                    )
                    and
                    data.get(
                        "product_url"
                    )
                ):

                    product_data[
                        number
                    ][
                        "product_url"
                    ] = (
                        data[
                            "product_url"
                        ]
                    )


                if (
                    not product_data[
                        number
                    ].get(
                        "card_image"
                    )
                    and
                    data.get(
                        "card_image"
                    )
                ):

                    product_data[
                        number
                    ][
                        "card_image"
                    ] = (
                        data[
                            "card_image"
                        ]
                    )


    # ========================================================
    # VISIT PRODUCT PAGES
    # ========================================================

    for number, data in product_data.items():

        product_url = data.get(
            "product_url"
        )


        image_url = None


        if product_url:

            image_url = get_product_page_image(
                product_url
            )


        # Αν δεν βρούμε full product image,
        # χρησιμοποιούμε την εικόνα από το card.

        if not image_url:

            image_url = data.get(
                "card_image"
            )


        if image_url:

            catalog[
                number
            ] = image_url


    # ========================================================
    # SEARCH FALLBACK ΓΙΑ ΟΣΑ ΛΕΙΠΟΥΝ
    # ========================================================

    for number in range(
        1,
        31
    ):

        if number in catalog:

            continue


        image_url = search_product(
            number
        )


        if image_url:

            catalog[
                number
            ] = image_url


    print()
    print(
        "IZNOGOUD CATALOG:"
    )
    print(
        f"Found {len(catalog)}/30 covers"
    )
    print()


    return catalog


# ============================================================
# PUBLIC FUNCTION
# ============================================================

@lru_cache(maxsize=50)
def get_iznogoud_cover(
    number
):

    try:

        number = int(
            number
        )

    except Exception:

        return None


    if (
        number < 1
        or
        number > 30
    ):

        return None


    catalog = build_catalog()


    return catalog.get(
        number
    )
