from flask import Flask, render_template, redirect, Response
from functools import lru_cache
from bs4 import BeautifulSoup
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
# ΑΣΤΕΡΙΞ - ΜΑΜΟΥΘ COMIX
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


asterix_comics = []

for number, title in enumerate(
    asterix_titles,
    start=1
):

    asterix_comics.append(
        {
            "number": number,
            "title": title,
            "image": f"/cover/asterix/{number}"
        }
    )


# ============================================================
# ΟΛΑ ΤΑ COMICS
# ============================================================

comics_data = {

    "asterix": asterix_comics,

    "lucky-luke": [],

    "arkas": [],

    "idefix": []
}


# ============================================================
# ΒΡΙΣΚΟΥΜΕ ΕΞΩΦΥΛΛΑ ΑΠΟ ΜΑΜΟΥΘ
# ============================================================

@lru_cache(maxsize=1)
def get_mamouth_asterix_covers():

    covers = {}

    headers = {
        "User-Agent":
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120 Safari/537.36"
    }


    pages = [

        "https://mamouthcomix.gr/"
        "product-category/albums/asterix/",

        "https://mamouthcomix.gr/"
        "product-category/albums/asterix/page/2/",

        "https://mamouthcomix.gr/"
        "product-category/albums/asterix/page/3/",

        "https://mamouthcomix.gr/"
        "product-category/albums/asterix/page/4/",

        "https://mamouthcomix.gr/"
        "product-category/albums/asterix/page/5/",

        "https://mamouthcomix-eshop.gr/"
        "product-category/"
        "%CE%BA%CF%8C%CE%BC%CE%B9%CE%BE/"
        "%CE%B1%CF%83%CF%84%CE%B5%CF%81%CE%AF%CE%BE__"
        "%CE%BF%CE%B2%CE%B5%CE%BB%CE%AF%CE%BE/"
    ]


    for page_url in pages:

        try:

            response = requests.get(
                page_url,
                headers=headers,
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
                    or
                    product.select_one(
                        "h2"
                    )
                    or
                    product.select_one(
                        "h3"
                    )
                    or
                    product.select_one(
                        "h4"
                    )
                )


                if not title_element:
                    continue


                product_title = (
                    title_element
                    .get_text(
                        " ",
                        strip=True
                    )
                )


                match = re.search(
                    r"Αστερίξ\s*[-#:]?\s*(\d{1,2})",
                    product_title,
                    re.IGNORECASE
                )


                if not match:
                    continue


                number = int(
                    match.group(1)
                )


                if (
                    number < 1
                    or number > 41
                ):
                    continue


                image = product.find(
                    "img"
                )


                if not image:
                    continue


                image_url = (

                    image.get(
                        "data-lazy-src"
                    )

                    or image.get(
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

                    covers[number] = (
                        image_url
                        .replace(
                            "http://",
                            "https://"
                        )
                    )


        except Exception:

            continue


    return covers


# ============================================================
# FALLBACK - GOOGLE BOOKS
# ============================================================

@lru_cache(maxsize=100)
def google_books_cover(title):

    try:

        response = requests.get(

            "https://www.googleapis.com/"
            "books/v1/volumes",

            params={
                "q":
                    f'Αστερίξ "{title}"',
                "maxResults": 5,
                "langRestrict": "el"
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


            image_links = volume_info.get(
                "imageLinks",
                {}
            )


            image_url = (

                image_links.get(
                    "extraLarge"
                )

                or image_links.get(
                    "large"
                )

                or image_links.get(
                    "medium"
                )

                or image_links.get(
                    "thumbnail"
                )

                or image_links.get(
                    "smallThumbnail"
                )
            )


            if image_url:

                return (
                    image_url
                    .replace(
                        "http://",
                        "https://"
                    )
                )


    except Exception:

        pass


    return None


# ============================================================
# PLACEHOLDER ΑΝ ΔΕΝ ΒΡΕΘΕΙ ΕΞΩΦΥΛΛΟ
# ============================================================

def placeholder_cover(
    number,
    title
):

    safe_title = html.escape(
        title
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
            fill="#ffd60a"
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
            y="150"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="60"
            font-weight="bold"
            fill="#161616"
        >
            ΑΣΤΕΡΙΞ
        </text>

        <text
            x="300"
            y="245"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="65"
            font-weight="bold"
            fill="#ff3b30"
        >
            #{number}
        </text>

        <text
            x="300"
            y="390"
            text-anchor="middle"
            font-family="Arial"
            font-size="30"
            font-weight="bold"
            fill="#161616"
        >
            {safe_title[:28]}
        </text>

        <text
            x="300"
            y="650"
            text-anchor="middle"
            font-family="Arial Black, Arial"
            font-size="60"
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
# ROUTE ΓΙΑ ΤΑ ΕΞΩΦΥΛΛΑ
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


    image_url = (
        google_books_cover(
            title
        )
    )


    if image_url:

        return redirect(
            image_url
        )


    return placeholder_cover(
        number,
        title
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    all_comics = []


    for series_comics in (
        comics_data.values()
    ):

        all_comics.extend(
            series_comics
        )


    stats = {

        "total":
            len(all_comics),

        "owned": 0,

        "wishlist": 0,

        "duplicates": 0
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


    comics = comics_data.get(
        slug,
        []
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
