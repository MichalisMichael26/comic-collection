from flask import Flask, render_template, Response

from lucky_luke_data import (
    get_lucky_luke_comics as load_lucky_luke_comics
)

from idefix_data import (
    get_idefix_comics as load_idefix_comics
)

from arkas_data import (
    get_arkas_comics as load_arkas_comics
)

from iznogoud_data import (
    get_iznogoud_comics as load_iznogoud_comics
)

from rantanplan_data import (
    get_rantanplan_comics as load_rantanplan_comics
)

from sherlock_holmes_data import (
    get_sherlock_holmes_comics as load_sherlock_holmes_comics
)

from lucky_luke_covers import (
    get_lucky_luke_cover,
    get_lucky_luke_special_cover
)

from asterix_covers import (
    get_asterix_cover
)

import requests


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
    },

    {
        "name": "Ιζνογκούντ",
        "slug": "iznogoud"
    },

    {
        "name": "Ραντανπλάν",
        "slug": "rantanplan"
    },

    {
        "name": "Σέρλοκ Χολμς",
        "slug": "sherlock-holmes"
    }

]


# ============================================================
# ΑΣΤΕΡΙΞ
# ============================================================

ASTERIX_TITLES = [

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
    "Ο Αστερίξ στην Λουζιτανία"

]


def get_asterix_comics():

    comics = []

    for number, title in enumerate(
        ASTERIX_TITLES,
        start=1
    ):

        comics.append(
            {
                "number": number,
                "title": title,
                "image": f"/cover/asterix/{number}",
                "owned": False
            }
        )

    return comics


# ============================================================
# ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

def get_lucky_luke_comics():

    original = load_lucky_luke_comics()

    comics = []

    for comic in original:

        number = comic["number"]

        if number == "SPECIAL":

            image = "/cover/lucky-luke-special"

        else:

            image = (
                f"/cover/lucky-luke/{number}"
            )

        comics.append(
            {
                "number": number,
                "title": comic["title"],
                "image": image,
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# ΙΝΤΕΦΙΞ
# ============================================================

def get_idefix_comics():

    original = load_idefix_comics()

    comics = []

    for comic in original:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": comic.get(
                    "image",
                    ""
                ),
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# ΑΡΚΑΣ
# ============================================================

def get_arkas_comics():

    original = load_arkas_comics()

    comics = []

    for comic in original:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": comic.get(
                    "image",
                    ""
                ),
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# ΙΖΝΟΓΚΟΥΝΤ
# ============================================================

def get_iznogoud_comics():

    original = load_iznogoud_comics()

    comics = []

    for comic in original:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": comic.get(
                    "image",
                    ""
                ),
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# ΡΑΝΤΑΝΠΛΑΝ
# ============================================================

def get_rantanplan_comics():

    original = load_rantanplan_comics()

    comics = []

    for comic in original:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": comic.get(
                    "image",
                    ""
                ),
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# ΣΕΡΛΟΚ ΧΟΛΜΣ
# ============================================================

def get_sherlock_holmes_comics():

    original = (
        load_sherlock_holmes_comics()
    )

    comics = []

    for comic in original:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": comic.get(
                    "image",
                    ""
                ),
                "owned": comic.get(
                    "owned",
                    False
                )
            }
        )

    return comics


# ============================================================
# COMICS ΑΝΑ ΚΑΤΗΓΟΡΙΑ
# ============================================================

def get_comics(slug):

    if slug == "arkas":
        return get_arkas_comics()

    if slug == "lucky-luke":
        return get_lucky_luke_comics()

    if slug == "asterix":
        return get_asterix_comics()

    if slug == "idefix":
        return get_idefix_comics()

    if slug == "iznogoud":
        return get_iznogoud_comics()

    if slug == "rantanplan":
        return get_rantanplan_comics()

    if slug == "sherlock-holmes":
        return get_sherlock_holmes_comics()

    return []


# ============================================================
# ΟΛΑ ΤΑ COMICS
# ============================================================

def get_all_comics():

    all_comics = []

    for category in categories:

        comics = get_comics(
            category["slug"]
        )

        for comic in comics:

            item = comic.copy()

            item["series"] = (
                category["slug"]
            )

            item["series_name"] = (
                category["name"]
            )

            all_comics.append(
                item
            )

    return all_comics


# ============================================================
# GROUPS
# ============================================================

def get_comic_groups():

    groups = []

    for category in categories:

        groups.append(
            {
                "category": category,
                "comics": get_comics(
                    category["slug"]
                )
            }
        )

    return groups


# ============================================================
# REMOTE IMAGE
# ============================================================

def load_remote_image(image_url):

    if not image_url:

        return None


    headers = {

        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        )

    }


    if "comicstrip.gr" in image_url:

        headers["Referer"] = (
            "https://comicstrip.gr/"
        )


    elif "comicon-shop.gr" in image_url:

        headers["Referer"] = (
            "https://comicon-shop.gr/"
        )


    elif "mamouthcomix" in image_url:

        headers["Referer"] = (
            "https://mamouthcomix-eshop.gr/"
        )


    try:

        response = requests.get(
            image_url,
            headers=headers,
            timeout=15
        )


        if response.status_code != 200:

            return None


        content_type = (
            response.headers.get(
                "Content-Type",
                ""
            )
        )


        if not content_type.startswith(
            "image/"
        ):

            return None


        result = Response(
            response.content,
            content_type=content_type
        )


        result.headers[
            "Cache-Control"
        ] = (
            "public, max-age=86400"
        )


        return result


    except Exception:

        return None


# ============================================================
# PLACEHOLDER
# ============================================================

def placeholder_cover(
    text="NO COVER"
):

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
            y="350"
            text-anchor="middle"
            font-family="Arial"
            font-size="42"
            font-weight="bold"
            fill="#161616"
        >
            {text}
        </text>

        <text
            x="300"
            y="500"
            text-anchor="middle"
            font-family="Arial"
            font-size="70"
            font-weight="bold"
            fill="#ff3b30"
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
# COVER ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

@app.route(
    "/cover/lucky-luke/<int:number>"
)
def lucky_luke_cover_route(number):

    image_url = (
        get_lucky_luke_cover(
            number
        )
    )


    image = load_remote_image(
        image_url
    )


    if image:

        return image


    return placeholder_cover(
        f"LUCKY LUKE #{number}"
    )


# ============================================================
# SPECIAL ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

@app.route(
    "/cover/lucky-luke-special"
)
def lucky_luke_special_route():

    image_url = (
        get_lucky_luke_special_cover()
    )


    image = load_remote_image(
        image_url
    )


    if image:

        return image


    return placeholder_cover(
        "LUCKY LUKE"
    )


# ============================================================
# COVER ΑΣΤΕΡΙΞ
# ============================================================

@app.route(
    "/cover/asterix/<int:number>"
)
def asterix_cover_route(number):

    if number < 1 or number > 41:

        return "", 404


    image_url = (
        get_asterix_cover(
            number
        )
    )


    image = load_remote_image(
        image_url
    )


    if image:

        return image


    return placeholder_cover(
        f"ASTERIX #{number}"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    all_comics = get_all_comics()

    total = len(
        all_comics
    )

    owned = sum(
        1
        for comic in all_comics
        if comic.get(
            "owned",
            False
        )
    )


    stats = {

        "total": total,

        "owned": owned,

        "missing": (
            total - owned
        ),

        "duplicates": 0

    }


    return render_template(

        "dashboard.html",

        categories=categories,

        stats=stats,

        all_comics=all_comics

    )


# ============================================================
# ΜΟΥ ΛΕΙΠΟΥΝ
# ============================================================

@app.route("/missing")
def missing():

    return render_template(

        "missing.html",

        categories=categories,

        groups=get_comic_groups(),

        all_comics=get_all_comics()

    )


# ============================================================
# CATEGORY
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

        comics=comics,

        categories=categories

    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
