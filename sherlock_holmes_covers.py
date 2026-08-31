# ============================================================
# SHERLOCK HOLMES COVER SERVICE
# Ελληνική σειρά Μαμούθ #01 - #04
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


# ============================================================
# SETTINGS
# ============================================================

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

SHERLOCK_HOLMES_TITLES = {

    1: "Δεν Φοβάται Τίποτα",

    2: "Η Λέσχη των Ακραίων Σπορ",

    3: "Οι Άνθρωποι της Καμέλιας",

    4: 'Η Σκιά του "Μ"'

}


# ============================================================
# ΑΚΡΙΒΕΙΣ PRODUCT PAGES
# eFantasy - Ελληνικές εκδόσεις Μαμούθ
# ============================================================

SHERLOCK_PRODUCT_PAGES = {

    # --------------------------------------------------------
    # 01 - Δεν Φοβάται Τίποτα
    # --------------------------------------------------------

    1: (
        "https://www.efantasy.gr/el/"
        "%CF%80%CF%81%CE%BF%CF%8A%CF%8C%CE%BD%CF%84%CE%B1/"
        "comics/"
        "367679-"
        "%CF%83%CE%AD%CF%81%CE%BB%CE%BF%CE%BA-"
        "%CF%87%CE%BF%CE%BB%CE%BC%CF%82-1-"
        "%CE%B4%CE%B5%CE%BD-"
        "%CF%86%CE%BF%CE%B2%CE%AC%CF%84%CE%B1%CE%B9-"
        "%CF%84%CE%AF%CF%80%CE%BF%CF%84%CE%B1"
    ),


    # --------------------------------------------------------
    # 02 - Η Λέσχη των Ακραίων Σπορ
    # --------------------------------------------------------

    2: (
        "https://www.efantasy.gr/el/"
        "%CF%80%CF%81%CE%BF%CF%8A%CF%8C%CE%BD%CF%84%CE%B1/"
        "comics/"
        "367681-"
        "%CF%83%CE%AD%CF%81%CE%BB%CE%BF%CE%BA-"
        "%CF%87%CE%BF%CE%BB%CE%BC%CF%82-2-"
        "%CE%B7-"
        "%CE%BB%CE%AD%CF%83%CF%87%CE%B7-"
        "%CF%84%CF%89%CE%BD-"
        "%CE%B1%CE%BA%CF%81%CE%B1%CE%AF%CF%89%CE%BD-"
        "%CF%83%CF%80%CE%BF%CF%81"
    ),


    # --------------------------------------------------------
    # 03 - Οι Άνθρωποι της Καμέλιας
    # --------------------------------------------------------

    3: (
        "https://www.efantasy.gr/el/"
        "%CF%80%CF%81%CE%BF%CF%8A%CF%8C%CE%BD%CF%84%CE%B1/"
        "comics/"
        "367683-"
        "%CF%83%CE%AD%CF%81%CE%BB%CE%BF%CE%BA-"
        "%CF%87%CE%BF%CE%BB%CE%BC%CF%82-3-"
        "%CE%BF%CE%B9-"
        "%CE%AC%CE%BD%CE%B8%CF%81%CF%89%CF%80%CE%BF%CE%B9-"
        "%CF%84%CE%B7%CF%82-"
        "%CE%BA%CE%B1%CE%BC%CE%AD%CE%BB%CE%B9%CE%B1%CF%82"
    ),


    # --------------------------------------------------------
    # 04 - Η Σκιά του "Μ"
    # --------------------------------------------------------

    4: (
        "https://www.efantasy.gr/el/"
        "%CF%80%CF%81%CE%BF%CF%8A%CF%8C%CE%BD%CF%84%CE%B1/"
        "comics/"
        "367685-"
        "%CF%83%CE%AD%CF%81%CE%BB%CE%BF%CE%BA-"
        "%CF%87%CE%BF%CE%BB%CE%BC%CF%82-4-"
        "%CE%B7-"
        "%CF%83%CE%BA%CE%B9%CE%AC-"
        "%CF%84%CE%BF%CF%85-"
        "%CE%BC"
    )

}


# ============================================================
# COVER ΑΠΟ PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=10)
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
        # 1. OPEN GRAPH
        # ----------------------------------------------------

        image = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            image
            and
            image.get("content")
        ):

            image_url = image.get(
                "content"
            )


            if image_url:

                return urljoin(
                    product_url,
                    image_url
                )


        # ----------------------------------------------------
        # 2. TWITTER IMAGE
        # ----------------------------------------------------

        image = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            image
            and
            image.get("content")
        ):

            image_url = image.get(
                "content"
            )


            if image_url:

                return urljoin(
                    product_url,
                    image_url
                )


        # ----------------------------------------------------
        # 3. PRODUCT IMAGES
        # ----------------------------------------------------

        selectors = [

            ".product-image img",

            ".product-gallery img",

            ".product-main-image img",

            'img[itemprop="image"]',

            ".swiper-slide img"

        ]


        for selector in selectors:

            image = soup.select_one(
                selector
            )


            if not image:

                continue


            image_url = (

                image.get(
                    "data-src"
                )

                or image.get(
                    "data-lazy-src"
                )

                or image.get(
                    "data-zoom-image"
                )

                or image.get(
                    "src"
                )

            )


            if (
                image_url
                and
                not image_url.startswith(
                    "data:"
                )
            ):

                return urljoin(
                    product_url,
                    image_url
                )


    except Exception:

        return None


    return None


# ============================================================
# MAIN FUNCTION
# ============================================================

@lru_cache(maxsize=10)
def get_sherlock_holmes_cover(
    number
):

    if (
        number < 1
        or
        number > 4
    ):

        return None


    product_url = (
        SHERLOCK_PRODUCT_PAGES.get(
            number
        )
    )


    if not product_url:

        return None


    return get_cover_from_product_page(
        product_url
    )
