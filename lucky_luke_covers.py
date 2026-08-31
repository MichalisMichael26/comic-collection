# ============================================================
# LUCKY LUKE COVER SERVICE
# Καλύπτει ΟΛΑ τα τεύχη 01-90
# ============================================================

from functools import lru_cache
from urllib.parse import quote

from bs4 import BeautifulSoup

import requests
import re
import unicodedata


# ============================================================
# SETTINGS
# ============================================================

COMICON_BASE = "https://comicon-shop.gr"

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
# ΤΙΤΛΟΙ 01-90
# ============================================================

LUCKY_LUKE_TITLES = {

    1: "Ο ληστής με το ένα χέρι",
    2: "Με τη θηλειά στο λαιμό",
    3: "Ντάλτον Σίτυ",
    4: "Η θεραπεία των Ντάλτον",
    5: "Ο ελαφροχέρης",
    6: "Καλάμιτυ Τζέην",
    7: "Μαμά Ντάλτον",
    8: "Το καραβάνι",
    9: "Επικίνδυνη αποστολή",
    10: "Η άμαξα",

    11: "Οι Ντάλτον στα χιόνια",
    12: "Ο δικαστής",
    13: "Σάρα Μπερνάρ",
    14: "Μαύροι λόφοι",
    15: "Νταίηζυ Τάουν",
    16: "Τηγανίτες για τους Ντάλτον",
    17: "Νταίηλυ Σταρ",
    18: "Το τρυφερό πόδι",
    19: "Σύρματα στα λιβάδια",
    20: "Τζέσσε Τζαίημς",

    21: "Μπίλυ ο τρομερός",
    22: "Ο θησαυρός των Ντάλτον",
    23: "Κάνυον Απάτσι",
    24: "Στη σκιά των Ντέρικ",
    25: "Η απόδραση των Ντάλτον",
    26: "Η μνηστή του Λούκυ Λουκ",
    27: "Ο λευκός ιππότης",
    28: "Το σύρμα που τραγουδάει",
    29: "Η μπαλάντα των Ντάλτον",
    30: "Η κούρσα του Μισισιπή",

    31: "Οι Ντάλτον στους Ινδιάνους",
    32: "Αντιμέτωπος με τον Πατ Πόκερ",
    33: "Η εξαγορά των Ντάλτον",
    34: "Το 20ο σύνταγμα ιππικού",
    35: "Ο αυτοκράτωρ Σμιθ",
    36: "Η κληρονομιά του Ραντανπλάν",
    37: "Ο μεγάλος δούκας",
    38: "Νιτρογλυκερίνη",
    39: "Το κοράκι",
    40: "Το σιδερένιο άλογο",

    41: "Το καταραμένο ράντσο",
    42: "Προς την Οκλαχόμα",
    43: "Στα ίχνη των Ντάλτον",
    44: "Συναγερμός στους γαλαζοπόδαρους",
    45: "Φιλ Ντέφερ ο θεριστής",
    46: "Εναντίον Τζος Τζέημον",
    47: "Η πόλη φάντασμα",
    48: "Οι αντίπαλοι",
    49: "Το άλλοθι",
    50: "Οι παράνομοι",

    51: "Το τσίρκο",
    52: "Πόνυ Εξπρές",
    53: "Το ελιξήριο",
    54: "Τα ξαδέρφια των Ντάλτον",
    55: "Επικίνδυνο πέρασμα",
    56: "Κίτρινος πυρετός",
    57: "Ροντέο",
    58: "Η αμνησία των Ντάλτον",
    59: "Κυνήγι φαντασμάτων",
    60: "Αριζόνα",

    61: "Η επιστροφή του Τζόε η σκανδάλη",
    62: "Οι Ντάλτον σε γάμο",
    63: "Η γέφυρα του Μισισιπή",
    64: "Μπελ Σταρ",
    65: "Κλοντάικ",
    66: "Ένας σεΐχης στο Φαρ Ουέστ",
    67: "Παντρεύεται ο Λούκυ",
    68: "Ο.Κ. Κοράλ",
    69: "Ο Μακ στους Ινδιάνους",
    70: "Μαρσέλ Ντάλτον",

    71: "Ο μπόμπιρας Λούκυ",
    72: "Οκλαχόμα Τζιμ",
    73: "Ο προφήτης",
    74: "Ο ζωγράφος",
    75: "Ο θρύλος της Δύσης",
    76: "Η ωραία Προβένς",
    77: "Οι Ντάλτον στην κρεμάλα",
    78: "Ο άνθρωπος από την Ουάσινγκτον",
    79: "Λούκυ Λουκ εναντίον Πίνκερτον",
    80: "Μοναχικός καβαλάρης",

    81: "Οι Ντάλτον θείοι",
    82: "Η γη της επαγγελίας",
    83: "Λούκυ Κιντ Μαθητευόμενος καουμπόυ",
    84: "Ένας καουμπόυ στο Παρίσι",
    85: "Επικίνδυνο λάσο",
    86: "Λούκυ Κιντ Αταξία και τιμωρία",
    87: "Μπελάδες στις φυτείες",
    88: "Μάθε τέχνη κι άστηνε",
    89: "Η Κιβωτός του Ραντανπλάν",
    90: "Τα Βαρέλια της Οργής"

}


# ============================================================
# DIRECT URLs ΠΟΥ ΕΧΟΥΜΕ ΗΔΗ ΔΟΚΙΜΑΣΕΙ
# ============================================================

STATIC_COVERS = {

    1: (
        "https://mamouthcomix-eshop.gr/"
        "wp-content/uploads/2022/07/"
        "%CE%BB%CE%BB-01.png"
    ),

    2: (
        "https://cdn.slidesharecdn.com/"
        "ss_thumbnails/"
        "02-230414110324-cc954bd8-thumbnail.jpg"
        "?fit=bounds&height=640&width=640"
    ),

    4: (
        "https://production-metabook-covers-7."
        "ams3.digitaloceanspaces.com/"
        "files/b9/86/"
        "9dad759f-ba9c-4c9f-87bc-d5013c815d93.jpg"
    ),

    5: (
        "https://i.ebayimg.com/"
        "images/g/-qwAAOSwEeFVDLef/"
        "s-l1200.jpg"
    ),

    6: (
        "https://bcdn.vendora.gr/"
        "0/4b/92/"
        "4b924e5a4cfe0ba9c2a4182ca0e61e1eae7977d2.jpg"
        "?class=lsq"
    ),

    7: (
        "https://a.scdn.gr/"
        "images/sku_main_images/003871/3871251/"
        "xlarge_20210608170616_mama_ntalton.jpeg"
    ),

    8: (
        "https://mamouthcomix.gr/"
        "wp-content/uploads/2018/02/"
        "LL-08.jpg"
    ),

    9: (
        "https://mamouthcomix.gr/"
        "wp-content/uploads/2018/02/"
        "LL-09-298x300.jpg"
    ),

    10: (
        "https://www.e-shop.gr/"
        "images/BKS/"
        "BKS.0762069.jpg"
    ),

    33: (
        "https://comicstrip.gr/"
        "image/catalog/product/"
        "lucky-luke-33-h-e3agora-twn-ntalton.jpg"
    )

}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = str(text).lower()

    normalized = unicodedata.normalize(
        "NFD",
        text
    )

    normalized = "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )

    normalized = re.sub(
        r"[^a-zα-ω0-9]+",
        " ",
        normalized
    )

    return normalized.strip()


# ============================================================
# WORDPRESS SLUG
# ============================================================

def make_slug(title):

    title = title.lower().strip()

    replacements = {
        "&": " και ",
        "’": "",
        "'": "",
        "΄": "",
        "«": "",
        "»": "",
        '"': "",
        ".": "",
        ",": "",
        ":": "",
        ";": "",
        "?": "",
        "!": "",
        "(": "",
        ")": "",
        "/": " ",
        "\\": " ",
    }

    for old, new in replacements.items():

        title = title.replace(
            old,
            new
        )


    title = re.sub(
        r"\s+",
        "-",
        title
    )


    title = re.sub(
        r"-+",
        "-",
        title
    )


    return title.strip("-")


# ============================================================
# OG IMAGE ΑΠΟ ΣΕΛΙΔΑ ΠΡΟΪΟΝΤΟΣ
# ============================================================

@lru_cache(maxsize=200)
def extract_cover_from_page(
    page_url
):

    try:

        response = requests.get(
            page_url,
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

        og = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            og
            and
            og.get("content")
        ):

            return og.get(
                "content"
            )


        # ----------------------------------------------------
        # Twitter
        # ----------------------------------------------------

        twitter = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            twitter
            and
            twitter.get("content")
        ):

            return twitter.get(
                "content"
            )


        # ----------------------------------------------------
        # WooCommerce
        # ----------------------------------------------------

        image = soup.select_one(
            "img.wp-post-image"
        )


        if image:

            return (
                image.get(
                    "data-large_image"
                )
                or
                image.get(
                    "data-src"
                )
                or
                image.get(
                    "src"
                )
            )


        # ----------------------------------------------------
        # Gallery
        # ----------------------------------------------------

        image = soup.select_one(
            ".woocommerce-product-gallery img"
        )


        if image:

            return (
                image.get(
                    "data-large_image"
                )
                or
                image.get(
                    "src"
                )
            )


    except Exception:

        return None


    return None


# ============================================================
# COMICON SEARCH FALLBACK
# ============================================================

@lru_cache(maxsize=200)
def search_comicon_product(
    title
):

    try:

        search_url = (
            COMICON_BASE
            + "/?s="
            + quote(title)
            + "&post_type=product"
        )


        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=12
        )


        if response.status_code != 200:

            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        wanted = normalize_text(
            title
        )


        links = soup.select(
            'a[href*="/shop/"]'
        )


        best_url = None


        for link in links:

            href = link.get(
                "href"
            )

            text = link.get_text(
                " ",
                strip=True
            )


            if not href:

                continue


            normalized_text = (
                normalize_text(
                    text
                )
            )


            # Αν ο τίτλος ταιριάζει καλά
            if (
                wanted
                and
                (
                    wanted
                    in normalized_text
                    or
                    normalized_text
                    in wanted
                )
            ):

                return href


            if best_url is None:

                best_url = href


        return best_url


    except Exception:

        return None


# ============================================================
# MICROLINK FALLBACK
# Παίρνει metadata/image όταν το Render δυσκολεύεται
# να διαβάσει απευθείας τη σελίδα.
# ============================================================

@lru_cache(maxsize=200)
def microlink_cover(
    page_url
):

    if not page_url:

        return None


    try:

        response = requests.get(

            "https://api.microlink.io",

            params={
                "url": page_url
            },

            timeout=15

        )


        if response.status_code != 200:

            return None


        data = response.json()


        image = (
            data
            .get("data", {})
            .get("image", {})
            .get("url")
        )


        return image


    except Exception:

        return None


# ============================================================
# COVER ΓΙΑ ΕΝΑ ΤΕΥΧΟΣ
# ============================================================

@lru_cache(maxsize=100)
def get_lucky_luke_cover(
    number
):

    # --------------------------------------------------------
    # Έλεγχος αριθμού
    # --------------------------------------------------------

    if (
        number < 1
        or
        number > 90
    ):

        return None


    # --------------------------------------------------------
    # 1. STATIC URL
    # --------------------------------------------------------

    static = STATIC_COVERS.get(
        number
    )


    if static:

        return static


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = LUCKY_LUKE_TITLES.get(
        number
    )


    if not title:

        return None


    # --------------------------------------------------------
    # 2. DIRECT PRODUCT URL
    # --------------------------------------------------------

    slug = make_slug(
        title
    )


    product_url = (
        COMICON_BASE
        + "/shop/"
        + quote(
            slug,
            safe="-"
        )
    )


    image = extract_cover_from_page(
        product_url
    )


    if image:

        return image


    # --------------------------------------------------------
    # 3. COMICON SEARCH
    # --------------------------------------------------------

    found_product = (
        search_comicon_product(
            title
        )
    )


    if found_product:

        image = (
            extract_cover_from_page(
                found_product
            )
        )


        if image:

            return image


    # --------------------------------------------------------
    # 4. MICROLINK DIRECT PAGE
    # --------------------------------------------------------

    image = microlink_cover(
        product_url
    )


    if image:

        return image


    # --------------------------------------------------------
    # 5. MICROLINK SEARCH RESULT PAGE
    # --------------------------------------------------------

    if found_product:

        image = microlink_cover(
            found_product
        )


        if image:

            return image


    return None


# ============================================================
# SPECIAL
# ============================================================

SPECIAL_TITLE = (
    "Ο Ντόλης Δεν Απαντάει Πιά"
)


@lru_cache(maxsize=1)
def get_lucky_luke_special_cover():

    slug = make_slug(
        SPECIAL_TITLE
    )


    product_url = (
        COMICON_BASE
        + "/shop/"
        + quote(
            slug,
            safe="-"
        )
    )


    image = extract_cover_from_page(
        product_url
    )


    if image:

        return image


    found_product = (
        search_comicon_product(
            SPECIAL_TITLE
        )
    )


    if found_product:

        image = (
            extract_cover_from_page(
                found_product
            )
        )


        if image:

            return image


    image = microlink_cover(
        product_url
    )


    if image:

        return image


    if found_product:

        return microlink_cover(
            found_product
        )


    return None
