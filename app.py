from flask import Flask, render_template, redirect, Response
from functools import lru_cache
from bs4 import BeautifulSoup
from lucky_luke_data import get_lucky_luke_comics

from urllib.parse import urljoin

import requests
import re
import html


app = Flask(__name__)


# ============================================================
# ΚΑΤΗΓΟΡΙΕΣ
# ============================================================

categories = [

    {
        "name": "Αρκάς",
        "slug": "arkas"
    },

    {
        "name": "Λούκυ Λουκ",
        "slug": "lucky-luke"
    },

    {
        "name": "Αστερίξ",
        "slug": "asterix"
    },

    {
        "name": "Ιντεφίξ",
        "slug": "idefix"
    }

]


# ============================================================
# ΑΣΤΕΡΙΞ
# ============================================================

asterix_titles = [

    "Ο Αγώνας των Αρχηγών",
    "Οβελίξ & Σια",
    "Ο Αστερίξ στην Ισπανία",
    "Ο Αστερίξ και οι Γότθοι",
    "Αστερίξ και Κλεοπάτρα",
    "Η Διχόνοια",
    "Η Κατοικία των Θεών",
    "Ο Μάντης",
    "Ο Γύρος της Γαλατίας",
    "Αστερίξ ο Γαλάτης",

    "Ο Αστερίξ στους Βέλγους",
    "Ο Αστερίξ στην Κορσική",
    "Ο Αστερίξ Μονομάχος",
    "Ο Αστερίξ και οι Νορμανδοί",
    "Οι Δάφνες του Καίσαρα",
    "Το Χρυσό Δρεπάνι",
    "Ο Αστερίξ στους Βρετανούς",
    "Ο Αστερίξ και η Χύτρα",
    "Η Ασπίδα της Αρβέρνης",
    "Ο Αστερίξ στους Ελβετούς",

    "Το Δώρο του Καίσαρα",
    "Ρόδο και Ξίφος",
    "Το Μεγάλο Ταξίδι",
    "Ο Αστερίξ Λεγεωνάριος",
    "Ο Αστερίξ στους Ολυμπιακούς Αγώνες",
    "Η Μεγάλη Τάφρος",
    "Η Οδύσσεια του Αστερίξ",
    "Ο Γιος του Αστερίξ",
    "Ο Αστερίξ και η Χαλαλίμα",
    "Η Γαλέρα του Οβελίξ",

    "Ο Αστερίξ και η Λατραβιάτα",
    "Ο Αστερίξ και η Επιστροφή των Γαλατών",
    "Και ο Ουρανός έπεσε στο κεφάλι τους",
    "Τα Γενέθλια των Αστερίξ και Οβελίξ",
    "Ο Αστερίξ στους Πίκτους",
    "Ο Πάπυρος του Καίσαρα",
    "Ο Αστερίξ και ο Υπεριταλικός",
    "Η Κόρη του Βερσινζεντορίξ",
    "Ο Αστερίξ και ο Γρύπας",
    "Η Λευκή Ίριδα",
    "Ο Αστερίξ στη Λουζιτανία"

]


def get_asterix_comics():

    comics = []

    for number, title in enumerate(
        asterix_titles,
        start=1
    ):

        comics.append(
            {
                "number": number,
                "title": title,
                "image": f"/cover/asterix/{number}"
            }
        )

    return comics


# ============================================================
# HEADERS
# ============================================================

HEADERS = {

    "User-Agent":
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"

}


# ============================================================
# ΑΣΤΕΡΙΞ - ΕΞΩΦΥΛΛΑ
# ΔΕΝ ΑΛΛΑΖΟΥΜΕ ΤΗ ΛΕΙΤΟΥΡΓΙΑ ΤΟΥ
# ============================================================

@lru_cache(maxsize=1)
def get_mamouth_asterix_covers():

    covers = {}


    pages = [

        "https://mamouthcomix.gr/product-category/albums/asterix/",

        "https://mamouthcomix.gr/product-category/albums/asterix/page/2/",

        "https://mamouthcomix.gr/product-category/albums/asterix/page/3/",

        "https://mamouthcomix.gr/product-category/albums/asterix/page/4/",

        "https://mamouthcomix.gr/product-category/albums/asterix/page/5/"

    ]


    for page_url in pages:

        try:

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=8
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

                title_element = (

                    product.select_one(
                        ".woocommerce-loop-product__title"
                    )

                    or product.select_one("h2")

                    or product.select_one("h3")

                )


                if not title_element:
                    continue


                product_title = (
                    title_element.get_text(
                        " ",
                        strip=True
                    )
                )


                match = re.search(
                    r"Αστερίξ\s*[-#:]?\s*0?(\d{1,2})",
                    product_title,
                    re.IGNORECASE
                )


                if not match:
                    continue


                number = int(
                    match.group(1)
                )


                image = product.find(
                    "img"
                )


                if not image:
                    continue


                image_url = (

                    image.get("data-lazy-src")

                    or image.get("data-src")

                    or image.get("data-original")

                    or image.get("src")

                )


                if (
                    image_url
                    and
                    not image_url.startswith("data:")
                ):

                    covers[number] = (
                        image_url.replace(
                            "http://",
                            "https://"
                        )
                    )


        except Exception:

            continue


    return covers


# ============================================================
# ΒΟΗΘΗΤΙΚΟ:
# ΒΡΙΣΚΕΙ ΤΗΝ ΚΑΛΥΤΕΡΗ ΕΙΚΟΝΑ
# ΣΕ ΚΑΡΤΑ ΠΡΟΪΟΝΤΟΣ
# ============================================================

def get_best_product_image(
    product,
    page_url
):

    image = product.find("img")


    if not image:
        return None


    # Πρώτα δοκιμάζουμε srcset γιατί συνήθως
    # περιέχει την καλύτερη ανάλυση

    srcsets = [

        image.get("data-srcset"),

        image.get("srcset")

    ]


    for srcset in srcsets:

        if not srcset:
            continue


        candidates = []


        for item in srcset.split(","):

            item = item.strip()


            if not item:
                continue


            candidate = (
                item.split(" ")[0].strip()
            )


            if candidate:
                candidates.append(candidate)


        if candidates:

            image_url = candidates[-1]


            if not image_url.startswith("data:"):

                return urljoin(
                    page_url,
                    image_url
                )


    # Αν δεν υπάρχει srcset,
    # δοκιμάζουμε τα κλασικά attributes

    possible_urls = [

        image.get("data-lazy-src"),

        image.get("data-src"),

        image.get("data-original"),

        image.get("src")

    ]


    for image_url in possible_urls:

        if (
            image_url
            and
            not image_url.startswith("data:")
        ):

            return urljoin(
                page_url,
                image_url
            )


    return None


# ============================================================
# ΛΟΥΚΥ ΛΟΥΚ
# ΠΑΙΡΝΟΥΜΕ IMAGE + PRODUCT URL
# ============================================================

@lru_cache(maxsize=1)
def get_mamouth_lucky_luke_catalog():

    catalog = {}


    base_url = (
        "https://mamouthcomix.gr/"
        "product-category/albums/%CE%BB%CE%BB/"
    )


    # Η σειρά βρίσκεται σε 10 σελίδες.

    for page in range(1, 11):

        if page == 1:

            page_url = base_url

        else:

            page_url = (
                base_url
                + f"page/{page}/"
            )


        try:

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=10
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

                title_element = (

                    product.select_one(
                        ".woocommerce-loop-product__title"
                    )

                    or product.select_one("h2")

                    or product.select_one("h3")

                )


                if not title_element:
                    continue


                full_title = (
                    title_element.get_text(
                        " ",
                        strip=True
                    )
                )


                # ----------------------------
                # PRODUCT URL
                # ----------------------------

                product_link = (

                    product.select_one(
                        "a.woocommerce-LoopProduct-link"
                    )

                    or product.select_one(
                        'a[href*="/product/"]'
                    )

                )


                product_url = None


                if (
                    product_link
                    and
                    product_link.get("href")
                ):

                    product_url = urljoin(
                        page_url,
                        product_link.get("href")
                    )


                # ----------------------------
                # ΕΙΚΟΝΑ ΑΠΟ ΤΗΝ ΚΑΡΤΑ
                # ----------------------------

                image_url = get_best_product_image(
                    product,
                    page_url
                )


                # ----------------------------
                # SPECIAL
                # ----------------------------

                if (
                    "Ντόλης δεν απαντάει"
                    in full_title
                ):

                    catalog["SPECIAL"] = {

                        "title":
                            "Ο Ντόλης δεν απαντάει πιά",

                        "image":
                            image_url,

                        "product_url":
                            product_url

                    }

                    continue


                # ----------------------------
                # ΑΡΙΘΜΗΜΕΝΑ ΤΕΥΧΗ
                # ----------------------------

                match = re.search(

                    r"Λούκυ\s*Λουκ\s*"
                    r"[-#:]?\s*"
                    r"0?(\d{1,2})",

                    full_title,

                    re.IGNORECASE

                )


                if not match:
                    continue


                number = int(
                    match.group(1)
                )


                if (
                    number < 1
                    or number > 89
                ):
                    continue


                catalog[number] = {

                    "image":
                        image_url,

                    "product_url":
                        product_url

                }


        except Exception:

            continue


    return catalog


# ============================================================
# ΑΝ ΔΕΝ ΠΑΡΟΥΜΕ ΕΙΚΟΝΑ ΑΠΟ ΤΗΝ ΚΑΡΤΑ,
# ΜΠΑΙΝΟΥΜΕ ΣΤΗ ΣΕΛΙΔΑ ΤΟΥ ΠΡΟΪΟΝΤΟΣ
# ΚΑΙ ΠΑΙΡΝΟΥΜΕ OG:IMAGE
# ============================================================

@lru_cache(maxsize=150)
def get_product_page_cover(
    product_url
):

    if not product_url:
        return None


    try:

        response = requests.get(
            product_url,
            headers=HEADERS,
            timeout=10
        )


        if response.status_code != 200:
            return None


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # OpenGraph image

        og_image = soup.select_one(
            'meta[property="og:image"]'
        )


        if (
            og_image
            and og_image.get("content")
        ):

            return urljoin(
                product_url,
                og_image.get("content")
            )


        # Twitter image

        twitter_image = soup.select_one(
            'meta[name="twitter:image"]'
        )


        if (
            twitter_image
            and twitter_image.get("content")
        ):

            return urljoin(
                product_url,
                twitter_image.get("content")
            )


        # WooCommerce main image

        main_image = soup.select_one(
            "img.wp-post-image"
        )


        if main_image:

            image_url = (

                main_image.get("data-large_image")

                or main_image.get("data-src")

                or main_image.get("src")

            )


            if image_url:

                return urljoin(
                    product_url,
                    image_url
                )


    except Exception:

        pass


    return None


# ============================================================
# ΤΟ RENDER ΚΑΤΕΒΑΖΕΙ ΤΗΝ ΕΙΚΟΝΑ
# ΚΑΙ ΤΗ ΣΕΡΒΙΡΕΙ ΣΤΟ APP
# ============================================================

@lru_cache(maxsize=200)
def fetch_remote_image(
    image_url
):

    if not image_url:
        return None


    try:

        headers = dict(HEADERS)

        headers["Referer"] = (
            "https://mamouthcomix.gr/"
        )


        response = requests.get(
            image_url,
            headers=headers,
            timeout=12
        )


        if response.status_code != 200:
            return None


        content_type = response.headers.get(
            "Content-Type",
            ""
        )


        if not content_type.startswith(
            "image/"
        ):

            return None


        return (
            response.content,
            content_type
        )


    except Exception:

        return None


def make_image_response(
    image_url
):

    result = fetch_remote_image(
        image_url
    )


    if not result:
        return None


    content, content_type = result


    response = Response(
        content,
        content_type=content_type
    )


    response.headers[
        "Cache-Control"
    ] = "public, max-age=86400"


    return response


# ============================================================
# GOOGLE BOOKS FALLBACK
# ============================================================

@lru_cache(maxsize=300)
def google_books_cover(
    series,
    title
):

    try:

        response = requests.get(

            "https://www.googleapis.com/"
            "books/v1/volumes",

            params={

                "q":
                    f'{series} "{title}"',

                "maxResults":
                    5

            },

            timeout=8

        )


        if response.status_code != 200:
            return None


        data = response.json()


        for item in data.get(
            "items",
            []
        ):

            volume_info = item.get(
                "volumeInfo",
                {}
            )


            images = volume_info.get(
                "imageLinks",
                {}
            )


            image_url = (

                images.get("extraLarge")

                or images.get("large")

                or images.get("medium")

                or images.get("thumbnail")

                or images.get("smallThumbnail")

            )


            if image_url:

                return image_url.replace(
                    "http://",
                    "https://"
                )


    except Exception:

        pass


    return None


# ============================================================
# PLACEHOLDER
# ============================================================

def placeholder_cover(
    series,
    number,
    title,
    background="#ffd60a"
):

    safe_series = html.escape(
        str(series)
    )


    safe_title = html.escape(
        str(title)
    )


    if len(safe_title) > 30:

        safe_title = (
            safe_title[:30]
            + "..."
        )


    svg = f"""
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="600"
        height="800"
        viewBox="0 0 600 800"
    >

        <rect
            width="600"
            height="800"
            fill="{background}"
        />

        <rect
            x="20"
            y="20"
            width="560"
            height="760"
            fill="none"
            stroke="#161616"
            stroke-width="18"
        />

        <text
            x="300"
            y="145"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="48"
            font-weight="bold"
            fill="#161616"
        >
            {safe_series}
        </text>

        <text
            x="300"
            y="250"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="68"
            font-weight="bold"
            fill="#ff3b30"
        >
            #{number}
        </text>

        <text
            x="300"
            y="405"
            text-anchor="middle"
            font-family="Arial"
            font-size="25"
            font-weight="bold"
            fill="#161616"
        >
            {safe_title}
        </text>

        <text
            x="300"
            y="660"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="58"
            font-weight="bold"
            fill="#2979ff"
        >
            POW!
        </text>

    </svg>
    """


    return Response(
        svg,
        mimetype="image/svg+xml"
    )


# ============================================================
# COVER - ΑΣΤΕΡΙΞ
# ΙΔΙΑ ΛΕΙΤΟΥΡΓΙΑ ΟΠΩΣ ΠΡΙΝ
# ============================================================

@app.route(
    "/cover/asterix/<int:number>"
)
def asterix_cover(number):

    if (
        number < 1
        or number > len(
            asterix_titles
        )
    ):

        return "", 404


    covers = (
        get_mamouth_asterix_covers()
    )


    image_url = covers.get(
        number
    )


    if image_url:

        return redirect(
            image_url
        )


    title = (
        asterix_titles[
            number - 1
        ]
    )


    image_url = google_books_cover(
        "Αστερίξ",
        title
    )


    if image_url:

        return redirect(
            image_url
        )


    return placeholder_cover(
        "ΑΣΤΕΡΙΞ",
        number,
        title,
        "#ffd60a"
    )


# ============================================================
# COVER - ΛΟΥΚΥ ΛΟΥΚ
# ΝΕΑ ΔΙΟΡΘΩΜΕΝΗ ΛΕΙΤΟΥΡΓΙΑ
# ============================================================

@app.route(
    "/cover/lucky-luke/<int:number>"
)
def lucky_luke_cover(number):

    if (
        number < 1
        or number > 89
    ):

        return "", 404


    comics = (
        get_lucky_luke_comics()
    )


    comic = next(

        (
            item
            for item in comics
            if item["number"] == number
        ),

        None

    )


    if comic is None:

        return "", 404


    catalog = (
        get_mamouth_lucky_luke_catalog()
    )


    data = catalog.get(
        number,
        {}
    )


    # 1.
    # Πρώτα εικόνα από τον κατάλογο

    image_url = data.get(
        "image"
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    # 2.
    # Αν δεν βρεθεί,
    # μπαίνουμε στο προϊόν

    product_url = data.get(
        "product_url"
    )


    image_url = (
        get_product_page_cover(
            product_url
        )
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    # 3.
    # Google Books fallback

    image_url = google_books_cover(
        "Λούκυ Λουκ",
        comic["title"]
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    # 4.
    # Μόνο αν αποτύχουν όλα

    return placeholder_cover(
        "ΛΟΥΚΥ ΛΟΥΚ",
        number,
        comic["title"],
        "#9bdcff"
    )


# ============================================================
# SPECIAL ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

@app.route(
    "/cover/lucky-luke-special"
)
def lucky_luke_special_cover():

    title = (
        "Ο Ντόλης δεν απαντάει πιά"
    )


    catalog = (
        get_mamouth_lucky_luke_catalog()
    )


    data = catalog.get(
        "SPECIAL",
        {}
    )


    image_url = data.get(
        "image"
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    product_url = data.get(
        "product_url"
    )


    image_url = (
        get_product_page_cover(
            product_url
        )
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    image_url = google_books_cover(
        "Λούκυ Λουκ",
        title
    )


    image_response = (
        make_image_response(
            image_url
        )
    )


    if image_response:

        return image_response


    return placeholder_cover(
        "ΛΟΥΚΥ ΛΟΥΚ",
        "SPECIAL",
        title,
        "#9bdcff"
    )


# ============================================================
# COMICS ΑΝΑ ΚΑΤΗΓΟΡΙΑ
# ============================================================

def get_comics(
    slug
):

    if slug == "asterix":

        return (
            get_asterix_comics()
        )


    if slug == "lucky-luke":

        return (
            get_lucky_luke_comics()
        )


    if slug == "arkas":

        return []


    if slug == "idefix":

        return []


    return []


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    total = (

        len(
            get_asterix_comics()
        )

        +

        len(
            get_lucky_luke_comics()
        )

    )


    stats = {

        "total":
            total,

        "owned":
            0,

        "wishlist":
            0,

        "duplicates":
            0

    }


    return render_template(

        "dashboard.html",

        categories=categories,

        stats=stats

    )


# ============================================================
# ΚΑΤΗΓΟΡΙΑ
# ============================================================

@app.route(
    "/category/<slug>"
)
def category(slug):

    selected_category = next(

        (
            item
            for item in categories
            if item["slug"] == slug
        ),

        None

    )


    if selected_category is None:

        return (
            "Η κατηγορία δεν βρέθηκε.",
            404
        )


    comics = get_comics(
        slug
    )


    return render_template(

        "category.html",

        category=selected_category,

        comics=comics

    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
