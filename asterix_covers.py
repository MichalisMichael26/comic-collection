# ============================================================
# ASTERIX COVER SERVICE
# Ελληνική σειρά Μαμούθ #01 - #41
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

BASE_URL = "https://comicstrip.gr"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),
    "Accept-Language": "el-GR,el;q=0.9,en;q=0.8"
}


# ============================================================
# ΕΛΛΗΝΙΚΗ ΑΡΙΘΜΗΣΗ ΑΣΤΕΡΙΞ
# ============================================================

ASTERIX_TITLES = {

    1: "Ο Αγώνας των Αρχηγών",
    2: "Οβελίξ & ΣΙΑ",
    3: "Ο Αστερίξ στην Ισπανία",
    4: "Ο Αστερίξ και οι Γότθοι",
    5: "Αστερίξ και Κλεοπάτρα",
    6: "Η Διχόνοια",
    7: "Η Κατοικία των Θεών",
    8: "Ο Μάντης",
    9: "Ο Γύρος της Γαλατίας",
    10: "Αστερίξ ο Γαλάτης",

    11: "Ο Αστερίξ στους Βέλγους",
    12: "Ο Αστερίξ στην Κορσική",
    13: "Ο Αστερίξ Μονομάχος",
    14: "Ο Αστερίξ και οι Νορμανδοί",
    15: "Οι Δάφνες του Καίσαρα",
    16: "Το Χρυσό Δρεπάνι",
    17: "Ο Αστερίξ στους Βρετανούς",
    18: "Ο Αστερίξ και η Χύτρα",
    19: "Η Ασπίδα της Αρβέρνης",
    20: "Ο Αστερίξ στους Ελβετούς",

    21: "Το Δώρο του Καίσαρα",
    22: "Ρόδο και Ξίφος",
    23: "Το Μεγάλο Ταξίδι",
    24: "Ο Αστερίξ Λεγεωνάριος",
    25: "Ο Αστερίξ στους Ολυμπιακούς Αγώνες",
    26: "Η Μεγάλη Τάφρος",
    27: "Η Οδύσσεια του Αστερίξ",
    28: "Ο Γιος του Αστερίξ",
    29: "Ο Αστερίξ και η Χαλαλίμα",
    30: "Η Γαλέρα του Οβελίξ",

    31: "Ο Αστερίξ και η Λατραβιάτα",
    32: "Ο Αστερίξ και η Επιστροφή των Γαλατών",
    33: "Και ο Ουρανός έπεσε στο κεφάλι τους",
    34: "Τα Γενέθλια των Αστερίξ και Οβελίξ",
    35: "Ο Αστερίξ στους Πίκτους",
    36: "Ο Πάπυρος του Καίσαρα",
    37: "Ο Αστερίξ και ο Υπεριταλικός",
    38: "Η Κόρη του Βερσινζεντορίξ",
    39: "Ο Αστερίξ και ο Γρύπας",
    40: "Η Λευκή Ίριδα",
    41: "Ο Αστερίξ στην Λουζιτανία"

}


# ============================================================
# TEXT NORMALIZATION
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
# ΕΛΕΓΧΟΣ ΟΤΙ ΕΙΝΑΙ Η ΣΩΣΤΗ ΒΑΣΙΚΗ ΣΕΙΡΑ
# ============================================================

def is_correct_issue(
    product_title,
    number
):

    if not product_title:

        return False


    title = normalize_text(
        product_title
    )


    # --------------------------------------------------------
    # Αποκλείουμε άλλες σειρές
    # --------------------------------------------------------

    forbidden = [

        "σκληροδετο",
        "hc",
        "κυπριακη",
        "κρητικα",
        "ποντιακα",
        "αρχαια ελληνικα",
        "λατινικα",
        "ολα για τον"

    ]


    for word in forbidden:

        if normalize_text(word) in title:

            return False


    # --------------------------------------------------------
    # Πρέπει να ξεκινά σαν:
    # Αστερίξ 01
    # Αστερίξ 02
    # κ.λπ.
    # --------------------------------------------------------

    number_two_digits = (
        f"{number:02d}"
    )


    patterns = [

        rf"^αστεριξ\s+{number_two_digits}\b",

        rf"^asterix\s+{number_two_digits}\b"

    ]


    for pattern in patterns:

        if re.search(
            pattern,
            title
        ):

            return True


    return False


# ============================================================
# ΕΙΚΟΝΑ ΑΠΟ PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=100)
def get_image_from_product_page(
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
        # OPEN GRAPH
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
        # TWITTER IMAGE
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
        # PRODUCT IMAGE
        # ----------------------------------------------------

        selectors = [

            ".thumbnails img",

            ".product-image img",

            "#content img",

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
# ΠΑΙΡΝΟΥΜΕ ΤΙΤΛΟ ΑΠΟ PRODUCT PAGE
# ============================================================

def get_page_title(
    soup
):

    heading = soup.select_one(
        "h1"
    )


    if heading:

        return heading.get_text(
            " ",
            strip=True
        )


    title = soup.select_one(
        "title"
    )


    if title:

        return title.get_text(
            " ",
            strip=True
        )


    return ""


# ============================================================
# ΕΥΡΕΣΗ PRODUCT ΣΤΟ COMICSTRIP
# ============================================================

@lru_cache(maxsize=100)
def find_product_url(
    number
):

    title = ASTERIX_TITLES.get(
        number
    )


    if not title:

        return None


    number_text = (
        f"{number:02d}"
    )


    # --------------------------------------------------------
    # Το query έχει αριθμό ΚΑΙ τίτλο.
    # Έτσι αποφεύγουμε όσο γίνεται λάθος έκδοση.
    # --------------------------------------------------------

    queries = [

        f"Αστερίξ {number_text} {title}",

        f"Αστερίξ {number_text}",

        title

    ]


    search_bases = [

        (
            BASE_URL
            +
            "/index.php"
            "?route=product/search"
            "&search="
        ),

        (
            BASE_URL
            +
            "/el-gr/index.php"
            "?route=product/search"
            "&search="
        )

    ]


    for query in queries:

        for search_base in search_bases:

            search_url = (
                search_base
                +
                quote(
                    query
                )
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


                # ============================================
                # Μερικές φορές το search μπορεί να μας
                # στείλει κατευθείαν στο product.
                # ============================================

                current_title = (
                    get_page_title(
                        soup
                    )
                )


                if is_correct_issue(
                    current_title,
                    number
                ):

                    return response.url


                # ============================================
                # PRODUCT CARDS
                # ============================================

                cards = soup.select(
                    ".product-thumb"
                )


                for card in cards:

                    link = (

                        card.select_one(
                            ".caption h4 a"
                        )

                        or card.select_one(
                            "h4 a"
                        )

                        or card.select_one(
                            "h3 a"
                        )

                    )


                    if not link:

                        continue


                    product_title = (
                        link.get_text(
                            " ",
                            strip=True
                        )
                    )


                    if not is_correct_issue(
                        product_title,
                        number
                    ):

                        continue


                    href = link.get(
                        "href"
                    )


                    if href:

                        return urljoin(
                            BASE_URL,
                            href
                        )


                # ============================================
                # FALLBACK: όλα τα links
                # ============================================

                links = soup.select(
                    'a[href]'
                )


                for link in links:

                    product_title = (
                        link.get_text(
                            " ",
                            strip=True
                        )
                    )


                    if not is_correct_issue(
                        product_title,
                        number
                    ):

                        continue


                    href = link.get(
                        "href"
                    )


                    if not href:

                        continue


                    return urljoin(
                        BASE_URL,
                        href
                    )


            except Exception:

                continue


    return None


# ============================================================
# IMAGE ΑΠΟ SEARCH CARD
# δεύτερος τρόπος
# ============================================================

@lru_cache(maxsize=100)
def find_image_in_search(
    number
):

    title = ASTERIX_TITLES.get(
        number
    )


    if not title:

        return None


    number_text = (
        f"{number:02d}"
    )


    query = (
        f"Αστερίξ {number_text} {title}"
    )


    search_url = (

        BASE_URL
        +
        "/index.php"
        "?route=product/search"
        "&search="
        +
        quote(query)

    )


    try:

        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=15
        )


        if response.status_code != 200:

            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        cards = soup.select(
            ".product-thumb"
        )


        for card in cards:

            link = (

                card.select_one(
                    ".caption h4 a"
                )

                or card.select_one(
                    "h4 a"
                )

                or card.select_one(
                    "h3 a"
                )

            )


            if not link:

                continue


            product_title = (
                link.get_text(
                    " ",
                    strip=True
                )
            )


            if not is_correct_issue(
                product_title,
                number
            ):

                continue


            image = card.select_one(
                "img"
            )


            if not image:

                continue


            srcset = (

                image.get(
                    "srcset"
                )

                or image.get(
                    "data-srcset"
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


                    if parts:

                        candidates.append(
                            parts[0]
                        )


                if candidates:

                    return urljoin(
                        BASE_URL,
                        candidates[-1]
                    )


            image_url = (

                image.get(
                    "data-src"
                )

                or image.get(
                    "data-original"
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
                    BASE_URL,
                    image_url
                )


    except Exception:

        return None


    return None


# ============================================================
# ΚΥΡΙΑ FUNCTION
# ============================================================

@lru_cache(maxsize=50)
def get_asterix_cover(
    number
):

    # --------------------------------------------------------
    # VALID NUMBER
    # --------------------------------------------------------

    if (
        number < 1
        or
        number > 41
    ):

        return None


    # --------------------------------------------------------
    # 1. Βρίσκουμε ακριβώς το product
    # --------------------------------------------------------

    product_url = (
        find_product_url(
            number
        )
    )


    if product_url:

        image = (
            get_image_from_product_page(
                product_url
            )
        )


        if image:

            return image


    # --------------------------------------------------------
    # 2. Fallback στην εικόνα του search card
    # --------------------------------------------------------

    image = (
        find_image_in_search(
            number
        )
    )


    if image:

        return image


    return None
