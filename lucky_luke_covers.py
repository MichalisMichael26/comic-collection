# ============================================================
# LUCKY LUKE COVER SERVICE
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin

from bs4 import BeautifulSoup

import requests
import re
import unicodedata


# ============================================================
# SOURCE
# ============================================================

BASE_URL = (
    "https://comicon-shop.gr/"
    "product-category/"
    "%CE%BC%CE%B1%CE%BC%CE%BF%CF%8D%CE%B8-%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
    "%CE%BC%CE%B5%CE%B3%CE%AC%CE%BB%CE%BF%CE%B9-%CE%AE%CF%81%CF%89%CE%B5%CF%82/"
    "%CE%BB%CE%BF%CF%8D%CE%BA%CF%85-%CE%BB%CE%BF%CF%85%CE%BA"
)


HEADERS = {

    "User-Agent":
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36",

    "Accept-Language":
        "el-GR,el;q=0.9,en;q=0.8"

}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    text = str(text)

    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return (
        text
        .lower()
        .strip()
    )


# ============================================================
# ΒΡΙΣΚΟΥΜΕ ΑΡΙΘΜΟ ΤΕΥΧΟΥ
# ============================================================

def extract_issue_number(title):

    normalized = normalize_text(
        title
    )


    # Αποφεύγουμε διαφορετικές
    # σκληρόδετες εκδόσεις.

    if "σκληροδετο" in normalized:

        return None


    patterns = [

        r"λουκυ\s+λουκ\s*(?:νο|no|#)?\s*[-:]?\s*(\d{1,2})",

        r"λουκυ\s+λουκ.*?\s(\d{1,2})$"

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

            if 1 <= number <= 90:

                return number


    return None


# ============================================================
# ΠΑΙΡΝΟΥΜΕ IMAGE ΑΠΟ PRODUCT CARD
# ============================================================

def get_image_from_product(
    product,
    page_url
):

    image = product.find(
        "img"
    )


    if image is None:

        return None


    # --------------------------------------------------------
    # srcset
    # --------------------------------------------------------

    srcset = (

        image.get(
            "data-srcset"
        )

        or image.get(
            "srcset"
        )

    )


    if srcset:

        candidates = []


        for item in srcset.split(
            ","
        ):

            item = item.strip()


            if not item:

                continue


            parts = item.split()


            if not parts:

                continue


            candidate = parts[0]


            if (
                candidate
                and
                not candidate.startswith(
                    "data:"
                )
            ):

                candidates.append(
                    candidate
                )


        if candidates:

            return urljoin(
                page_url,
                candidates[-1]
            )


    # --------------------------------------------------------
    # normal / lazy src
    # --------------------------------------------------------

    possible_urls = [

        image.get(
            "data-lazy-src"
        ),

        image.get(
            "data-src"
        ),

        image.get(
            "data-original"
        ),

        image.get(
            "src"
        )

    ]


    for image_url in possible_urls:

        if (
            image_url
            and
            not image_url.startswith(
                "data:"
            )
        ):

            return urljoin(
                page_url,
                image_url
            )


    return None


# ============================================================
# PRODUCT PAGE IMAGE
# ============================================================

@lru_cache(maxsize=150)
def get_product_page_image(
    product_url
):

    if not product_url:

        return None


    try:

        response = requests.get(
            product_url,
            headers=HEADERS,
            timeout=12
        )


        if response.status_code != 200:

            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # ----------------------------------------------------
        # OpenGraph
        # ----------------------------------------------------

        og_image = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            og_image
            and
            og_image.get(
                "content"
            )
        ):

            return urljoin(
                product_url,
                og_image.get(
                    "content"
                )
            )


        # ----------------------------------------------------
        # Twitter
        # ----------------------------------------------------

        twitter_image = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            twitter_image
            and
            twitter_image.get(
                "content"
            )
        ):

            return urljoin(
                product_url,
                twitter_image.get(
                    "content"
                )
            )


        # ----------------------------------------------------
        # WooCommerce main image
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
        # WooCommerce gallery
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
# ΔΗΜΙΟΥΡΓΟΥΜΕ ΚΑΤΑΛΟΓΟ ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

@lru_cache(maxsize=1)
def get_lucky_luke_cover_catalog():

    catalog = {}


    # Δοκιμάζουμε αρκετές σελίδες
    # ώστε να βρούμε όλα τα προϊόντα.

    for page_number in range(
        1,
        8
    ):


        if page_number == 1:

            page_url = BASE_URL


        else:

            page_url = (
                BASE_URL
                +
                f"/page/{page_number}/"
            )


        try:

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=15
            )


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

                continue


            for product in products:


                # ============================================
                # TITLE
                # ============================================

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

                    continue


                title = (
                    title_element
                    .get_text(
                        " ",
                        strip=True
                    )
                )


                normalized_title = (
                    normalize_text(
                        title
                    )
                )


                # Δεν μας ενδιαφέρουν
                # προϊόντα εκτός Lucky Luke.

                if (
                    "λουκυ λουκ"
                    not in normalized_title
                    and
                    "ντολης"
                    not in normalized_title
                ):

                    continue


                # ============================================
                # PRODUCT URL
                # ============================================

                link_element = (

                    product.select_one(
                        "a.woocommerce-LoopProduct-link"
                    )

                    or product.select_one(
                        'a[href*="/shop/"]'
                    )

                    or product.select_one(
                        'a[href*="/product/"]'
                    )

                    or product.find(
                        "a"
                    )

                )


                product_url = None


                if (
                    link_element
                    and
                    link_element.get(
                        "href"
                    )
                ):

                    product_url = urljoin(
                        page_url,
                        link_element.get(
                            "href"
                        )
                    )


                # ============================================
                # IMAGE
                # ============================================

                image_url = (
                    get_image_from_product(
                        product,
                        page_url
                    )
                )


                # ============================================
                # SPECIAL
                # ============================================

                if (
                    "ντολης δεν απανταει"
                    in normalized_title
                ):

                    catalog[
                        "SPECIAL"
                    ] = {

                        "title":
                            title,

                        "image":
                            image_url,

                        "product_url":
                            product_url

                    }

                    continue


                # ============================================
                # NUMBER
                # ============================================

                number = (
                    extract_issue_number(
                        title
                    )
                )


                if number is None:

                    continue


                # ============================================
                # SAVE
                # ============================================

                if number not in catalog:

                    catalog[
                        number
                    ] = {

                        "title":
                            title,

                        "image":
                            image_url,

                        "product_url":
                            product_url

                    }


        except Exception:

            # Αν μία σελίδα αποτύχει,
            # συνεχίζουμε στην επόμενη.

            continue


    return catalog


# ============================================================
# ΠΑΙΡΝΟΥΜΕ COVER ΑΡΙΘΜΗΜΕΝΟΥ ΤΕΥΧΟΥ
# ============================================================

@lru_cache(maxsize=100)
def get_lucky_luke_cover(
    number
):

    catalog = (
        get_lucky_luke_cover_catalog()
    )


    data = catalog.get(
        number
    )


    if not data:

        return None


    # --------------------------------------------------------
    # 1. Εικόνα από category page
    # --------------------------------------------------------

    image_url = data.get(
        "image"
    )


    if image_url:

        return image_url


    # --------------------------------------------------------
    # 2. Εικόνα από product page
    # --------------------------------------------------------

    product_url = data.get(
        "product_url"
    )


    return get_product_page_image(
        product_url
    )


# ============================================================
# SPECIAL
# ============================================================

@lru_cache(maxsize=1)
def get_lucky_luke_special_cover():

    catalog = (
        get_lucky_luke_cover_catalog()
    )


    data = catalog.get(
        "SPECIAL"
    )


    if not data:

        return None


    image_url = data.get(
        "image"
    )


    if image_url:

        return image_url


    return get_product_page_image(
        data.get(
            "product_url"
        )
    )
