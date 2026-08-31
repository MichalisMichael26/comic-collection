# ============================================================
# RANTANPLAN COVER SERVICE
# Ελληνική σειρά Μαμούθ #01 - #17
# ============================================================

from functools import lru_cache
from urllib.parse import quote, urljoin

from bs4 import BeautifulSoup

import requests
import re
import unicodedata


# ============================================================
# SETTINGS
# ============================================================

BASE_URL = "https://mamouthcomix-eshop.gr"

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
# ΤΙΤΛΟΙ
# ============================================================

RANTANPLAN_TITLES = {

    1: "Η Μασκώτ",

    2: "Ο Νονός",

    3: "Ο Ραντανπλάν Όμηρος",

    4: "Ο Κλόουν",

    5: "Ο Φυγάς",

    6: "Ο Αγγελιοφόρος",

    7: "Ο Ατσίδας",

    8: "Οι Εγκέφαλοι",

    9: "Το Σπίρτο",

    10: "Ο Καταφερτζής",

    11: "Η Καμήλα",

    12: "Το Ξεφτέρι",

    13: "Το Μεγάλο Ταξίδι",

    14: "Η Πεντάμορφη και το Τέρας",

    15: "Ο Τσίφτης",

    16: "Τα Χριστούγεννα του Ραντανπλάν",

    17: "Επί ποδός πολέμου"

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
        if unicodedata.category(character) != "Mn"
    )

    text = text.lower()

    text = re.sub(
        r"[^a-zα-ω0-9]+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# ΒΡΙΣΚΟΥΜΕ ΑΡΙΘΜΟ ΑΠΟ ΤΙΤΛΟ
# ============================================================

def extract_number(text):

    if not text:

        return None


    normalized = normalize_text(
        text
    )


    patterns = [

        r"ραντανπλαν\s*0?(\d{1,2})",

        r"ραντανπλαν\s*#\s*0?(\d{1,2})"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            normalized
        )


        if match:

            number = int(
                match.group(1)
            )


            if 1 <= number <= 17:

                return number


    return None


# ============================================================
# ΕΛΕΓΧΟΣ PRODUCT
# ============================================================

def product_matches(
    title,
    number
):

    if not title:

        return False


    normalized = normalize_text(
        title
    )


    if "ραντανπλαν" not in normalized:

        return False


    found_number = extract_number(
        title
    )


    if found_number == number:

        return True


    wanted_title = normalize_text(
        RANTANPLAN_TITLES.get(
            number,
            ""
        )
    )


    if (
        wanted_title
        and
        wanted_title in normalized
    ):

        return True


    return False


# ============================================================
# ΠΑΙΡΝΟΥΜΕ COVER ΑΠΟ PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=30)
def get_cover_from_product_page(
    product_url
):

    if not product_url:

        return None


    try:

        response = requests.get(
            product_url,
            headers=HEADERS,
            timeout=15
        )


        if response.status_code != 200:

            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # ----------------------------------------------------
        # 1. OG IMAGE
        # ----------------------------------------------------

        image = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            image
            and
            image.get("content")
        ):

            return urljoin(
                product_url,
                image.get("content")
            )


        # ----------------------------------------------------
        # 2. TWITTER
        # ----------------------------------------------------

        image = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            image
            and
            image.get("content")
        ):

            return urljoin(
                product_url,
                image.get("content")
            )


        # ----------------------------------------------------
        # 3. WOOCOMMERCE MAIN IMAGE
        # ----------------------------------------------------

        image = soup.select_one(
            "img.wp-post-image"
        )


        if image:

            image_url = (

                image.get(
                    "data-large_image"
                )

                or image.get(
                    "data-src"
                )

                or image.get(
                    "src"
                )

            )


            if image_url:

                return urljoin(
                    product_url,
                    image_url
                )


        # ----------------------------------------------------
        # 4. GALLERY
        # ----------------------------------------------------

        image = soup.select_one(
            ".woocommerce-product-gallery img"
        )


        if image:

            image_url = (

                image.get(
                    "data-large_image"
                )

                or image.get(
                    "data-src"
                )

                or image.get(
                    "src"
                )

            )


            if image_url:

                return urljoin(
                    product_url,
                    image_url
                )


    except Exception:

        return None


    return None


# ============================================================
# SEARCH PRODUCT
# ============================================================

@lru_cache(maxsize=30)
def find_product_url(
    number
):

    if number < 1 or number > 17:

        return None


    title = RANTANPLAN_TITLES.get(
        number
    )


    queries = [

        f"Ραντανπλάν {number:02d}",

        f"Ραντανπλάν {number}",

        f"Ραντανπλάν {number:02d} {title}",

        f"Ραντανπλάν {title}"

    ]


    for query in queries:

        search_url = (

            BASE_URL
            +
            "/?s="
            +
            quote(query)
            +
            "&post_type=product"

        )


        try:

            response = requests.get(
                search_url,
                headers=HEADERS,
                timeout=15
            )


            if response.status_code != 200:

                continue


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            # ================================================
            # PRODUCT CARDS
            # ================================================

            products = soup.select(
                "li.product"
            )


            for product in products:

                link = (

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


                if not link:

                    continue


                product_title = link.get_text(
                    " ",
                    strip=True
                )


                if not product_matches(
                    product_title,
                    number
                ):

                    continue


                anchor = (

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


                if (
                    anchor
                    and
                    anchor.get("href")
                ):

                    return urljoin(
                        search_url,
                        anchor.get("href")
                    )


            # ================================================
            # FALLBACK ΟΛΑ ΤΑ LINKS
            # ================================================

            links = soup.select(
                'a[href*="/product/"]'
            )


            for link in links:

                product_title = link.get_text(
                    " ",
                    strip=True
                )


                if not product_matches(
                    product_title,
                    number
                ):

                    continue


                href = link.get(
                    "href"
                )


                if href:

                    return urljoin(
                        search_url,
                        href
                    )


        except Exception:

            continue


    return None


# ============================================================
# ΕΙΔΙΚΟ FALLBACK ΓΙΑ #17
# ============================================================

RANTANPLAN_17_URL = (
    "https://mamouthcomix-eshop.gr/"
    "product/"
    "%CF%81%CE%B1%CE%BD%CF%84%CE%B1%CE%BD%CF%80%CE%BB%CE%AC%CE%BD-17-"
    "%CE%B5%CF%80%CE%AF-%CF%80%CE%BF%CE%B4%CF%8C%CF%82-"
    "%CF%80%CE%BF%CE%BB%CE%AD%CE%BC%CE%BF%CF%85/"
)


# ============================================================
# MAIN FUNCTION
# ============================================================

@lru_cache(maxsize=20)
def get_rantanplan_cover(
    number
):

    if (
        number < 1
        or
        number > 17
    ):

        return None


    # --------------------------------------------------------
    # #17 - γνωστή επίσημη σελίδα
    # --------------------------------------------------------

    if number == 17:

        image = get_cover_from_product_page(
            RANTANPLAN_17_URL
        )


        if image:

            return image


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    product_url = find_product_url(
        number
    )


    if not product_url:

        return None


    return get_cover_from_product_page(
        product_url
    )
