# ============================================================
# ARKAS COVER SERVICE
# 27 σειρές / τίτλοι
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin

from bs4 import BeautifulSoup

import requests
import re
import unicodedata


# ============================================================
# SETTINGS
# ============================================================

PATAKIS_AUTHOR_URL = (
    "https://www.patakis.gr/"
    "person/person-16239/"
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
# ΟΙ 27 ΚΑΤΗΓΟΡΙΕΣ
# ============================================================

ARKAS_TITLES = {

    1: "Ο Κόκκορας",

    2: "Ο Ισοβίτης",

    3: "Χαμηλές Πτήσεις",

    4: "Καστράτο",

    5: "Η Ζωή Μετά",

    6: "Πειραματόζωα",

    7: "Show Business",

    8: "Ξυπνάς μέσα μου το ζώο",

    9: "Οι Συνομήλικοι",

    10: "Επικίνδυνα Νερά",

    11: "Μαλλί με Μαλλί",

    12: "Ο Καλός ο Λύκος",

    13: "Ο Παντελής και το Λιοντάρι",

    14: "Χίλιες Κυριακές",

    15: "Μετά την Καταστροφή",

    16: "Το Μικρό και το Μεγάλο",

    17: "Ο Προφήτης",

    18: "Ναπολέων και Ασημίνα",

    19: "Η Αποικία",

    20: "Τα Μαύρα",

    21: "Ζευγάρια",

    22: "Ζώα Πολιτικά",

    23: "Θηρία Ενήμερα",

    24: "Η Ρόζα",

    25: "Ο Ιεροεξεταστής του Αρκά",

    26: "Θανασάκης",

    27: "Ο Θεός αγαπάει τα χρυσόψαρα"

}


# ============================================================
# ΣΤΑΘΕΡΑ ΕΞΩΦΥΛΛΑ ΠΟΥ ΕΧΟΥΜΕ ΕΠΙΒΕΒΑΙΩΣΕΙ
# ============================================================

STATIC_COVERS = {

    # --------------------------------------------------------
    # 01 - Ο Κόκκορας
    # --------------------------------------------------------

    1: (
        "https://external.webstorage.gr/"
        "mmimages/image/40/15/76/93/"
        "0087977-264x264-800x800.jpg"
    ),


    # --------------------------------------------------------
    # 03 - Χαμηλές Πτήσεις
    # --------------------------------------------------------

    3: (
        "https://external.webstorage.gr/"
        "mmimages/image/20/50/58/95/"
        "1683863-264x264-800x800.jpg"
    ),


    # --------------------------------------------------------
    # 05 - Η Ζωή Μετά
    # --------------------------------------------------------

    5: (
        "https://d.scdn.gr/"
        "images/sku_main_images/"
        "037384/37384239/"
        "20220808155715_i_zoi_meta_epitomo.jpeg"
    ),


    # --------------------------------------------------------
    # 06 - Πειραματόζωα
    # --------------------------------------------------------

    6: (
        "https://external.webstorage.gr/"
        "mmimages/image/40/68/31/57/"
        "0203231-264x264-800x800-96x96-560x560.jpg"
    ),


    # --------------------------------------------------------
    # 07 - Show Business
    # --------------------------------------------------------

    7: (
        "https://www.lifo.gr/"
        "sites/default/files/styles/"
        "max_1920x1920/public/"
        "articles/2021-01-21/"
        "show_businnes.jpg"
        "?itok=Rk5y6WFg"
    ),


    # --------------------------------------------------------
    # 08 - Ξυπνάς μέσα μου το ζώο
    # --------------------------------------------------------

    8: (
        "https://d.scdn.gr/"
        "images/sku_main_images/"
        "000119/119107/"
        "xlarge_20220824162857_"
        "xypnas_mesa_mou_to_zoo.jpeg"
    ),


    # --------------------------------------------------------
    # 12 - Ο Καλός ο Λύκος
    # --------------------------------------------------------

    12: (
        "https://external.webstorage.gr/"
        "mmimages/image/70/37/29/60/"
        "0170119-264x264-800x800-96x96-560x560.jpg"
    ),


    # --------------------------------------------------------
    # 13 - Ο Παντελής και το Λιοντάρι
    # --------------------------------------------------------

    13: (
        "https://cdn-s3.insomnia.gr/"
        "monthly_2018_07/"
        "-1-638.jpg."
        "604657943bcb3d56af0d65ef4eb0b5f3.jpg"
    ),


    # --------------------------------------------------------
    # 14 - Χίλιες Κυριακές
    # --------------------------------------------------------

    14: (
        "https://bcdn.vendora.gr/"
        "0/07/93/"
        "07932f06833c818444188afee46ee013132cd314.jpg"
        "?class=lsq"
    ),


    # --------------------------------------------------------
    # 15 - Μετά την Καταστροφή
    # --------------------------------------------------------

    15: (
        "https://bcdn.vendora.gr/"
        "0/27/90/"
        "279024bc1d332b2cd10d198dd8ea1cc082e39439.jpg"
        "?class=lsq"
    ),


    # --------------------------------------------------------
    # 17 - Ο Προφήτης
    # --------------------------------------------------------

    17: (
        "https://comicon-shop.gr/"
        "wp-content/uploads/2021/02/"
        "%CE%BF-%CF%80%CF%81%CE%BF%CF%86%CE%AE%CF%84%CE%B7%CF%82.jpg"
    ),


    # --------------------------------------------------------
    # 19 - Η Αποικία
    # --------------------------------------------------------

    19: (
        "https://c.scdn.gr/"
        "images/sku_main_images/"
        "014522/14522477/"
        "20200219105454_i_apoikia.jpeg"
    ),


    # --------------------------------------------------------
    # 21 - Ζευγάρια
    # --------------------------------------------------------

    21: (
        "https://external.webstorage.gr/"
        "mmimages/image/96/51/94/29/"
        "1104410-264x264-800x800.jpg"
    )

}


# ============================================================
# ΟΝΟΜΑ ΠΟΥ ΨΑΧΝΟΥΜΕ ΣΤΙΣ ΕΚΔΟΣΕΙΣ ΠΑΤΑΚΗ
# ============================================================

PATAKIS_SEARCH_TERMS = {

    2: "Ο Ισοβίτης",

    4: "Καστράτο",

    5: "Η ζωή μετά",

    9: "Οι συνομήλικοι",

    10: "Επικίνδυνα νερά",

    11: "Μαλλί με μαλλί",

    16: "Το μικρό και το μεγάλο",

    17: "Ο Προφήτης",

    18: "Ναπολέων και Ασημίνα",

    20: "Τα μαύρα",

    22: "Ζώα πολιτικά",

    23: "Θηρία ενήμερα",

    24: "Η Ρόζα του Αρκά",

    25: "Ο Ιεροεξεταστής του Αρκά",

    26: "Θανασάκης του Αρκά",

    27: "Ο Θεός αγαπάει τα χρυσόψαρα"

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
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    text = text.lower()

    text = re.sub(
        r"[^a-zα-ω0-9]+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# ΚΑΤΑΛΟΓΟΣ ΒΙΒΛΙΩΝ ΠΑΤΑΚΗ
# ============================================================

@lru_cache(maxsize=1)
def get_patakis_catalog():

    catalog = []


    try:

        response = requests.get(
            PATAKIS_AUTHOR_URL,
            headers=HEADERS,
            timeout=15
        )


        if response.status_code != 200:

            return catalog


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        links = soup.select(
            'a[href*="/books/"]'
        )


        seen = set()


        for link in links:

            href = link.get(
                "href"
            )


            if not href:

                continue


            title = link.get_text(
                " ",
                strip=True
            )


            if not title:

                # Πολλές κάρτες έχουν
                # το title σε parent element.

                parent = link.parent


                if parent:

                    title = parent.get_text(
                        " ",
                        strip=True
                    )


            if not title:

                continue


            full_url = urljoin(
                PATAKIS_AUTHOR_URL,
                href
            )


            key = (
                normalize_text(title),
                full_url
            )


            if key in seen:

                continue


            seen.add(
                key
            )


            catalog.append(
                {
                    "title": title,
                    "normalized":
                        normalize_text(title),
                    "url": full_url
                }
            )


    except Exception:

        return []


    return catalog


# ============================================================
# ΒΡΙΣΚΟΥΜΕ PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=40)
def find_patakis_product(
    number
):

    wanted = PATAKIS_SEARCH_TERMS.get(
        number
    )


    if not wanted:

        return None


    wanted_normalized = (
        normalize_text(
            wanted
        )
    )


    catalog = get_patakis_catalog()


    # --------------------------------------------------------
    # 1. Πλήρες match
    # --------------------------------------------------------

    for item in catalog:

        if (
            wanted_normalized
            in item["normalized"]
        ):

            return item["url"]


    # --------------------------------------------------------
    # 2. Match λέξεων
    # --------------------------------------------------------

    wanted_words = set(
        wanted_normalized.split()
    )


    best_url = None
    best_score = 0


    for item in catalog:

        product_words = set(
            item["normalized"].split()
        )


        score = len(
            wanted_words
            &
            product_words
        )


        if score > best_score:

            best_score = score
            best_url = item["url"]


    # Θέλουμε τουλάχιστον 2 κοινές λέξεις.
    if best_score >= 2:

        return best_url


    return None


# ============================================================
# ΕΞΩΦΥΛΛΟ ΑΠΟ PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=50)
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

            return urljoin(
                product_url,
                image.get("content")
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

            return urljoin(
                product_url,
                image.get("content")
            )


        # ----------------------------------------------------
        # 3. PRODUCT IMAGE
        # ----------------------------------------------------

        selectors = [

            ".product-image img",

            ".book-image img",

            ".product-detail img",

            ".product-gallery img",

            'img[itemprop="image"]'

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
# MAIN
# ============================================================

@lru_cache(maxsize=40)
def get_arkas_cover(
    number
):

    if (
        number < 1
        or
        number > 27
    ):

        return None


    # --------------------------------------------------------
    # 1. ΣΤΑΘΕΡΟ ΕΠΙΒΕΒΑΙΩΜΕΝΟ URL
    # --------------------------------------------------------

    static_cover = (
        STATIC_COVERS.get(
            number
        )
    )


    if static_cover:

        return static_cover


    # --------------------------------------------------------
    # 2. ΕΠΙΣΗΜΕΣ ΕΚΔΟΣΕΙΣ ΠΑΤΑΚΗ
    # --------------------------------------------------------

    product_url = (
        find_patakis_product(
            number
        )
    )


    if product_url:

        image = (
            get_cover_from_product_page(
                product_url
            )
        )


        if image:

            return image


    return None
