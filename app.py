from flask import Flask, render_template, url_for
from pathlib import Path


# ============================================================
# DATA
# ============================================================

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


# ============================================================
# APP
# ============================================================

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


# ============================================================
# ΤΟΠΙΚΟ COVER
# ============================================================

def get_local_cover(
    series,
    number
):

    folder = (
        Path(app.static_folder)
        /
        "covers"
        /
        series
    )


    # --------------------------------------------------------
    # SPECIAL
    # --------------------------------------------------------

    if str(number).upper() == "SPECIAL":

        filename_base = "special"

    else:

        try:

            filename_base = (
                f"{int(number):02d}"
            )

        except Exception:

            filename_base = str(number)


    # --------------------------------------------------------
    # ΠΙΘΑΝΑ FORMAT
    # --------------------------------------------------------

    extensions = [

        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif"

    ]


    for extension in extensions:

        filename = (
            filename_base
            +
            extension
        )


        full_path = (
            folder
            /
            filename
        )


        if full_path.exists():

            return url_for(
                "static",
                filename=(
                    f"covers/"
                    f"{series}/"
                    f"{filename}"
                )
            )


    # Δεν υπάρχει τοπικό cover.
    # ΔΕΝ ψάχνουμε online.

    return ""


# ============================================================
# ΑΣΤΕΡΙΞ
# ============================================================

def get_asterix_comics():

    comics = []


    for number, title in enumerate(
        ASTERIX_TITLES,
        start=1
    ):

        comics.append(
            {
                "number":
                    number,

                "title":
                    title,

                "image":
                    get_local_cover(
                        "asterix",
                        number
                    ),

                "owned":
                    False
            }
        )


    return comics


# ============================================================
# ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

def get_lucky_luke_comics():

    original = (
        load_lucky_luke_comics()
    )


    comics = []


    for comic in original:

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "lucky-luke",
                        number
                    ),

                "owned":
                    comic.get(
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

    original = (
        load_idefix_comics()
    )


    comics = []


    for comic in original:

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "idefix",
                        number
                    ),

                "owned":
                    comic.get(
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

    original = (
        load_iznogoud_comics()
    )


    comics = []


    for comic in original:

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "iznogoud",
                        number
                    ),

                "owned":
                    comic.get(
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

    original = (
        load_rantanplan_comics()
    )


    comics = []


    for comic in original:

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "rantanplan",
                        number
                    ),

                "owned":
                    comic.get(
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

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "sherlock-holmes",
                        number
                    ),

                "owned":
                    comic.get(
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

    original = (
        load_arkas_comics()
    )


    comics = []


    for comic in original:

        number = comic["number"]


        comics.append(
            {
                "number":
                    number,

                "title":
                    comic["title"],

                "image":
                    get_local_cover(
                        "arkas",
                        number
                    ),

                "owned":
                    comic.get(
                        "owned",
                        False
                    )
            }
        )


    return comics


# ============================================================
# GET COMICS
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
# ALL COMICS
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
                "category":
                    category,

                "comics":
                    get_comics(
                        category["slug"]
                    )
            }
        )


    return groups


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    all_comics = (
        get_all_comics()
    )


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

        "total":
            total,

        "owned":
            owned,

        "missing":
            total - owned,

        "duplicates":
            0

    }


    return render_template(

        "dashboard.html",

        categories=categories,

        stats=stats,

        all_comics=all_comics

    )


# ============================================================
# MISSING
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
def category(
    slug
):

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


    return render_template(

        "category.html",

        category=
            selected_category,

        comics=
            get_comics(slug),

        categories=
            categories

    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
