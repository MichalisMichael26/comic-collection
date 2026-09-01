# ============================================================
# IZNOGOUD COVER SERVICE
# Ελληνική σειρά Μαμούθ #01 - #30
#
# ΝΕΑ ΕΚΔΟΣΗ:
# 1. WooCommerce Store API
# 2. Γενικός κατάλογος comics
# 3. Search fallback
#
# ΟΛΑ γίνονται μόνο όταν τρέχει το download_covers.py.
# Το κανονικό app χρησιμοποιεί μετά τα τοπικά αρχεία.
# ============================================================

from functools import lru_cache
from urllib.parse import urljoin
import re
import unicodedata

import requests
from bs4 import BeautifulSoup


# ============================================================
# SETTINGS
# ============================================================

BASE_URL = "https://mamouthcomix-eshop.gr/"


STORE_API_URL = (
    BASE_URL
    + "wp-json/wc/store/v1/products"
)


COMICS_CATEGORY_URL = (
    BASE_URL
    + "product-category/"
    + "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
)


SEARCH_URL = BASE_URL


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),

    "Accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/json;q=0.9,"
        "*/*;q=0.8"
    ),

    "Accept-Language":
        "el-GR,el;q=0.9,en;q=0.8"

}


# ============================================================
# ΕΠΙΣΗΜΟΙ ΤΙΤΛΟΙ
# ============================================================

IZNOGOUD_TITLES = {

    1:
        "Ο μεγάλος Βεζίρης Ιζνογκούντ",

    2:
        "Οι συνωμοσίες του μεγάλου Βεζίρη Ιζνογκούντ",

    3:
        "Οι διακοπές του Χαλίφη",

    4:
        "Αστράκια για τον Ιζνογκούντ",

    5:
        "Ιζνογκούντ ο απαίσιος",

    6:
        "Ο μαγικός υπολογιστής",

    7:
        "Ένα καρότο για τον Ιζνογκούντ",

    8:
        "Η μέρα των τρελών",

    9:
        "Το μαγικό χαλί",

    10:
        "Ο μαινόμενος",

    11:
        "Το κεφάλι του Τούρκου του Ιζνογκούντ",

    12:
        "Μια νεράιδα για τον Ιζνογκούντ",

    13:
        "Θέλω να γίνω Χαλίφης στη θέση του Χαλίφη",

    14:
        "Ο συνένοχος του Ιζνογκούντ",

    15:
        "Ο Ιζνογκούντ επιτέλους Χαλίφης",

    16:
        "Ο Ιζνογκούντ και οι γυναίκες",

    17:
        "Η επέτειος του Ιζνογκούντ",

    18:
        "Τα παιδικά χρόνια του Ιζνογκούντ",

    19:
        "Η παγίδα της σειρήνας",

    20:
        "Οι επιστροφές του Ιζνογκούντ",

    21:
        "Οι εφιάλτες του Ιζνογκούντ - Τόμος 1",

    22:
        "Οι εφιάλτες του Ιζνογκούντ - Τόμος 2",

    23:
        "Οι εφιάλτες του Ιζνογκούντ - Τόμος 3",

    24:
        "Οι εφιάλτες του Ιζνογκούντ - Τόμος 4",

    25:
        "Ποιος σκότωσε το Χαλίφη;",

    26:
        "Το συμπαθητικό τέρας",

    27:
        "Το λάθος του προγόνου",

    28:
        "Οι Χίλιες και Μία Νύχτες του Χαλίφη",

    29:
        "Ο Ιζνογκούντ Πρόεδρος",

    30:
        "Από Πατέρα σε Γιο"

}


# ============================================================
# NORMALIZE TEXT
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
        if unicodedata.category(character) != "Mn"
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
# ΒΡΙΣΚΟΥΜΕ ISSUE NUMBER
# ============================================================

def extract_number(text):

    normalized = normalize_text(
        text
    )

    if "ιζνογκουντ" not in normalized:
        return None


    patterns = [

        r"ιζνογκουντ\s*#?\s*0?(\d{1,2})",

        r"ιζνογκουντ\s*[-–—]\s*0?(\d{1,2})",

        r"ιζνογκουντ.*?#\s*0?(\d{1,2})"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            normalized
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
# ΕΛΕΓΧΟΣ IMAGE URL
# ============================================================

def clean_image_url(
    image_url,
    base_url=BASE_URL
):

    if not image_url:
        return None

    image_url = str(
        image_url
    ).strip()

    if not image_url:
        return None

    if image_url.startswith(
        "data:"
    ):
        return None

    return urljoin(
        base_url,
        image_url
    )


# ============================================================
# 1. WOOCOMMERCE STORE API
# ============================================================

def get_catalog_from_store_api():

    catalog = {}


    searches = [

        "Ιζνογκούντ",

        "ΙΖΝΟΓΚΟΥΝΤ",

        "Iznogoud"

    ]


    for search_term in searches:

        try:

            response = requests.get(

                STORE_API_URL,

                params={
                    "search":
                        search_term,

                    "per_page":
                        100
                },

                headers=HEADERS,

                timeout=25

            )


            if response.status_code != 200:

                continue


            content_type = (
                response.headers
                .get(
                    "Content-Type",
                    ""
                )
                .lower()
            )


            if (
                "json"
                not in content_type
            ):

                continue


            products = response.json()


            if not isinstance(
                products,
                list
            ):

                continue


            for product in products:

                if not isinstance(
                    product,
                    dict
                ):

                    continue


                title = (
                    product.get(
                        "name"
                    )
                    or
                    ""
                )


                number = extract_number(
                    title
                )


                if number is None:

                    continue


                images = (
                    product.get(
                        "images"
                    )
                    or
                    []
                )


                image_url = None


                if (
                    isinstance(
                        images,
                        list
                    )
                    and
                    images
                ):

                    first_image = (
                        images[0]
                    )


                    if isinstance(
                        first_image,
                        dict
                    ):

                        image_url = (

                            first_image.get(
                                "src"
                            )

                            or first_image.get(
                                "thumbnail"
                            )

                        )


                image_url = clean_image_url(
                    image_url
                )


                if not image_url:

                    continue


                if number not in catalog:

                    catalog[number] = (
                        image_url
                    )


        except Exception:

            continue


    return catalog


# ============================================================
# HTML PRODUCT IMAGE
# ============================================================

def get_image_from_product_card(
    product,
    page_url
):

    image = product.select_one(
        "img"
    )


    if not image:

        return None


    candidates = [

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
            "data-original"
        ),

        image.get(
            "src"
        )

    ]


    for candidate in candidates:

        candidate = clean_image_url(
            candidate,
            page_url
        )


        if candidate:

            return candidate


    # --------------------------------------------------------
    # SRCSET FALLBACK
    # --------------------------------------------------------

    srcset = image.get(
        "srcset"
    )


    if srcset:

        parts = srcset.split(
            ","
        )


        # Συνήθως το τελευταίο είναι
        # η μεγαλύτερη διαθέσιμη εικόνα.

        for part in reversed(
            parts
        ):

            candidate = (
                part.strip()
                .split(" ")[0]
            )


            candidate = clean_image_url(
                candidate,
                page_url
            )


            if candidate:

                return candidate


    return None


# ============================================================
# HTML PRODUCT TITLE
# ============================================================

def get_title_from_product_card(
    product
):

    selectors = [

        ".woocommerce-loop-product__title",

        "h2",

        "h3",

        ".product-title",

        ".woocommerce-loop-product__link"

    ]


    for selector in selectors:

        element = product.select_one(
            selector
        )


        if not element:

            continue


        title = element.get_text(
            " ",
            strip=True
        )


        if title:

            return title


    return ""


# ============================================================
# 2. ΓΕΝΙΚΗ ΚΑΤΗΓΟΡΙΑ COMICS
# ============================================================

def get_catalog_from_comics_pages():

    catalog = {}


    # Ψάχνουμε αρκετές σελίδες,
    # επειδή ο Ιζνογκούντ μπορεί να είναι
    # μοιρασμένος σε όλο το catalog.

    for page in range(
        1,
        21
    ):


        if page == 1:

            url = (
                COMICS_CATEGORY_URL
            )


        else:

            url = (
                COMICS_CATEGORY_URL
                +
                f"page/{page}/"
            )


        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )


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

                products = soup.select(
                    ".product"
                )


            if not products:

                continue


            for product in products:

                title = (
                    get_title_from_product_card(
                        product
                    )
                )


                number = extract_number(
                    title
                )


                if number is None:

                    continue


                image_url = (
                    get_image_from_product_card(
                        product,
                        url
                    )
                )


                if not image_url:

                    continue


                if number not in catalog:

                    catalog[number] = (
                        image_url
                    )


        except Exception:

            continue


    return catalog


# ============================================================
# 3. WORDPRESS SEARCH FALLBACK
# ============================================================

def get_catalog_from_search():

    catalog = {}


    search_terms = [

        "Ιζνογκούντ",

        "ΙΖΝΟΓΚΟΥΝΤ"

    ]


    for search_term in search_terms:

        for page in range(
            1,
            6
        ):


            params = {

                "s":
                    search_term,

                "post_type":
                    "product"

            }


            if page > 1:

                params["paged"] = (
                    page
                )


            try:

                response = requests.get(

                    SEARCH_URL,

                    params=params,

                    headers=HEADERS,

                    timeout=20

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

                    products = soup.select(
                        ".product"
                    )


                if not products:

                    continue


                for product in products:

                    title = (
                        get_title_from_product_card(
                            product
                        )
                    )


                    number = extract_number(
                        title
                    )


                    if number is None:

                        continue


                    image_url = (
                        get_image_from_product_card(
                            product,
                            response.url
                        )
                    )


                    if not image_url:

                        continue


                    if number not in catalog:

                        catalog[number] = (
                            image_url
                        )


            except Exception:

                continue


    return catalog


# ============================================================
# 4. PRODUCT PAGE FALLBACK
# ============================================================

def get_product_links_from_html():

    links = {}


    for page in range(
        1,
        21
    ):


        if page == 1:

            url = (
                COMICS_CATEGORY_URL
            )


        else:

            url = (
                COMICS_CATEGORY_URL
                +
                f"page/{page}/"
            )


        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )


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

                continue


            for product in products:

                title = (
                    get_title_from_product_card(
                        product
                    )
                )


                number = extract_number(
                    title
                )


                if number is None:

                    continue


                link = (

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


                if not link:

                    continue


                href = link.get(
                    "href"
                )


                if not href:

                    continue


                if number not in links:

                    links[number] = (
                        urljoin(
                            url,
                            href
                        )
                    )


        except Exception:

            continue


    return links


# ============================================================
# COVER FROM PRODUCT PAGE
# ============================================================

@lru_cache(maxsize=100)
def get_cover_from_product_page(
    product_url
):

    if not product_url:

        return None


    try:

        response = requests.get(
            product_url,
            headers=HEADERS,
            timeout=20
        )


        if response.status_code != 200:

            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        selectors = [

            'meta[property="og:image"]',

            'meta[name="twitter:image"]',

            'meta[property="twitter:image"]'

        ]


        for selector in selectors:

            element = soup.select_one(
                selector
            )


            if (
                element
                and
                element.get(
                    "content"
                )
            ):

                image_url = clean_image_url(
                    element.get(
                        "content"
                    ),
                    product_url
                )


                if image_url:

                    return image_url


        image_selectors = [

            ".woocommerce-product-gallery img",

            "img.wp-post-image",

            ".product img"

        ]


        for selector in image_selectors:

            image = soup.select_one(
                selector
            )


            if not image:

                continue


            candidates = [

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


            for candidate in candidates:

                image_url = clean_image_url(
                    candidate,
                    product_url
                )


                if image_url:

                    return image_url


    except Exception:

        return None


    return None


# ============================================================
# BUILD FULL CATALOG
# ============================================================

@lru_cache(maxsize=1)
def get_iznogoud_catalog():

    catalog = {}


    # --------------------------------------------------------
    # 1. STORE API
    # --------------------------------------------------------

    api_catalog = (
        get_catalog_from_store_api()
    )


    catalog.update(
        api_catalog
    )


    # --------------------------------------------------------
    # 2. COMICS CATEGORY
    # --------------------------------------------------------

    if len(catalog) < 30:

        html_catalog = (
            get_catalog_from_comics_pages()
        )


        for number, image_url in (
            html_catalog.items()
        ):

            if number not in catalog:

                catalog[number] = (
                    image_url
                )


    # --------------------------------------------------------
    # 3. SEARCH
    # --------------------------------------------------------

    if len(catalog) < 30:

        search_catalog = (
            get_catalog_from_search()
        )


        for number, image_url in (
            search_catalog.items()
        ):

            if number not in catalog:

                catalog[number] = (
                    image_url
                )


    # --------------------------------------------------------
    # 4. PRODUCT PAGE
    # --------------------------------------------------------

    if len(catalog) < 30:

        product_links = (
            get_product_links_from_html()
        )


        for number, product_url in (
            product_links.items()
        ):

            if number in catalog:

                continue


            image_url = (
                get_cover_from_product_page(
                    product_url
                )
            )


            if image_url:

                catalog[number] = (
                    image_url
                )


    return catalog


# ============================================================
# MAIN FUNCTION
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


    catalog = (
        get_iznogoud_catalog()
    )


    return catalog.get(
        number
    )
