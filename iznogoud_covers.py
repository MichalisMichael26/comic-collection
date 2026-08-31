# ============================================================
# IZNOGOUD COVER SERVICE
# Ελληνική σειρά Μαμούθ #01 - #30
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
import re


# ============================================================
# SETTINGS
# ============================================================

CATEGORY_URL = (
    "https://mamouthcomix-eshop.gr/"
    "product-category/"
    "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
    "%CE%B9%CE%B6%CE%BD%CE%BF%CE%B3%CE%BA%CE%BF%CF%8D%CE%BD%CF%84/"
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
# ΕΠΙΣΗΜΟΙ ΤΙΤΛΟΙ #01 - #30
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
# ΒΡΙΣΚΟΥΜΕ ΤΟΝ ΑΡΙΘΜΟ ΑΠΟ ΤΟ PRODUCT TITLE
# ============================================================

def extract_number(text):

    if not text:

        return None

    match = re.search(
        r"Ιζνογκούντ\s*0?(\d{1,2})",
        text,
        re.IGNORECASE
    )

    if not match:

        return None

    number = int(
        match.group(1)
    )

    if 1 <= number <= 30:

        return number

    return None


# ============================================================
# ΚΑΤΑΛΟΓΟΣ PRODUCT URLS
# ============================================================

@lru_cache(maxsize=1)
def get_product_catalog():

    catalog = {}


    # Δοκιμάζουμε μέχρι 3 σελίδες.
    # Αν δεν υπάρχει η σελίδα απλά συνεχίζει.

    for page in range(
        1,
        4
    ):

        if page == 1:

            url = CATEGORY_URL

        else:

            url = (
                CATEGORY_URL
                +
                f"page/{page}/"
            )


        try:

            response = requests.get(
                url,
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


            for product in products:

                link = (

                    product.select_one(
                        "h2 a"
                    )

                    or product.select_one(
                        "h3 a"
                    )

                    or product.select_one(
                        ".woocommerce-loop-product__link"
                    )

                    or product.select_one(
                        'a[href*="/product/"]'
                    )

                )


                if not link:

                    continue


                title = link.get_text(
                    " ",
                    strip=True
                )


                number = extract_number(
                    title
                )


                if number is None:

                    continue


                href = link.get(
                    "href"
                )


                if not href:

                    continue


                if number not in catalog:

                    catalog[number] = urljoin(
                        url,
                        href
                    )


        except Exception:

            continue


    return catalog


# ============================================================
# COVER ΑΠΟ PRODUCT PAGE
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
        # 3. WOOCOMMERCE IMAGE
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
        # 4. PRODUCT GALLERY
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
# MAIN FUNCTION
# ============================================================

@lru_cache(maxsize=40)
def get_iznogoud_cover(
    number
):

    if (
        number < 1
        or
        number > 30
    ):

        return None


    catalog = get_product_catalog()


    product_url = catalog.get(
        number
    )


    if not product_url:

        return None


    return get_cover_from_product_page(
        product_url
    )
