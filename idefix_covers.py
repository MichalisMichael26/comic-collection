# ============================================================
# IDEFIX COVER SERVICE
# Ο Ιντεφίξ και οι Ανυπότακτοι
# Ελληνικές εκδόσεις
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
# ΑΚΡΙΒΕΙΣ ΣΕΛΙΔΕΣ ΤΩΝ 2 ΤΕΥΧΩΝ
# ============================================================

IDEFIX_PRODUCT_PAGES = {

    # --------------------------------------------------------
    # 01 - Κανένας οίκτος για τους Λατίνους
    # --------------------------------------------------------

    1: (
        "https://comicstrip.gr/"
        "el-gr/comics/katallhla-gia-paidia/"
        "o-intefi3-kai-oi-anypotaktoi-1%3A-"
        "kanenas-oiktos-gia-toys-latinoys"
    ),


    # --------------------------------------------------------
    # 02 - Ο Ιντεφίξ και ο Δρουίδης
    # --------------------------------------------------------

    2: (
        "https://comicstrip.gr/"
        "el-gr/comics/katallhla-gia-paidia/"
        "o-intefi3-kai-oi-anypotaktoi-2%3A-"
        "o-intefi3-kai-o-droyidhs"
    )

}


# ============================================================
# ΠΑΙΡΝΟΥΜΕ ΤΗΝ ΕΙΚΟΝΑ ΑΠΟ ΤΗ ΣΕΛΙΔΑ
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
        # 1. OPEN GRAPH IMAGE
        # ----------------------------------------------------

        og_image = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            og_image
            and
            og_image.get("content")
        ):

            return urljoin(
                product_url,
                og_image.get("content")
            )


        # ----------------------------------------------------
        # 2. TWITTER IMAGE
        # ----------------------------------------------------

        twitter_image = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            twitter_image
            and
            twitter_image.get("content")
        ):

            return urljoin(
                product_url,
                twitter_image.get("content")
            )


        # ----------------------------------------------------
        # 3. PRODUCT IMAGE
        # ----------------------------------------------------

        selectors = [

            ".thumbnails img",

            ".product-image img",

            "img.img-responsive"

        ]


        for selector in selectors:

            image = soup.select_one(
                selector
            )


            if not image:

                continue


            image_url = (

                image.get(
                    "data-large-image"
                )

                or image.get(
                    "data-zoom-image"
                )

                or image.get(
                    "data-src"
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

@lru_cache(maxsize=5)
def get_idefix_cover(
    number
):

    product_url = (
        IDEFIX_PRODUCT_PAGES.get(
            number
        )
    )


    if not product_url:

        return None


    return get_cover_from_product_page(
        product_url
    )
