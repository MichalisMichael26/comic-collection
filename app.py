from flask import Flask, render_template, url_for
from pathlib import Path


# ============================================================
# DATA - ΠΑΛΙΕΣ ΚΑΤΗΓΟΡΙΕΣ
# ============================================================

from lucky_luke_data import (
    get_lucky_luke_comics
    as load_lucky_luke_comics
)

from idefix_data import (
    get_idefix_comics
    as load_idefix_comics
)

from arkas_data import (
    get_arkas_comics
    as load_arkas_comics
)

from iznogoud_data import (
    get_iznogoud_comics
    as load_iznogoud_comics
)

from rantanplan_data import (
    get_rantanplan_comics
    as load_rantanplan_comics
)

from sherlock_holmes_data import (
    get_sherlock_holmes_comics
    as load_sherlock_holmes_comics
)


# ============================================================
# DATA - ΝΕΕΣ ΚΑΤΗΓΟΡΙΕΣ
# ============================================================

from zelda_data import (
    get_zelda_comics
    as load_zelda_comics
)

from dc_comics_data import (
    get_dc_comics
    as load_dc_comics
)

from marvel_data import (
    get_marvel_comics
    as load_marvel_comics
)

from marvel_graphic_novel_data import (
    get_marvel_graphic_novels
    as load_marvel_graphic_novels
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
        "slug": "arkas",
    },

    {
        "name": "Λούκυ Λουκ",
        "slug": "lucky-luke",
    },

    {
        "name": "Αστερίξ",
        "slug": "asterix",
    },

    {
        "name": "Ιντεφίξ",
        "slug": "idefix",
    },

    {
        "name": "Ιζνογκούντ",
        "slug": "iznogoud",
    },

    {
        "name": "Ραντανπλάν",
        "slug": "rantanplan",
    },

    {
        "name": "Σέρλοκ Χολμς",
        "slug": "sherlock-holmes",
    },

    # ========================================================
    # ΝΕΕΣ ΚΑΤΗΓΟΡΙΕΣ
    # ========================================================

    {
        "name": "Zelda",
        "slug": "zelda",
    },

    {
        "name": "DC Comics",
        "slug": "dc-comics",
    },

    {
        "name": "Marvel",
        "slug": "marvel",
    },

    {
        "name": "Marvel Graphic Novel",
        "slug": "marvel-graphic-novel",
    },

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
    "Ο Αστερίξ στην Λουζιτανία",

]


# ============================================================
# ΤΟΠΙΚΟ COVER
# ============================================================

def get_local_cover(
    series,
    number,
):

    folder = (
        Path(app.static_folder)
        / "covers"
        / series
    )

    # --------------------------------------------------------
    # SPECIAL
    # --------------------------------------------------------

    if str(number).upper() == "SPECIAL":

        filename_bases = [
            "special",
            "SPECIAL",
        ]

    else:

        try:

            int_number = int(
                number
            )

            # Υποστηρίζουμε:
            #
            # 001.jpg  -> νέα μορφή
            # 01.jpg   -> παλιά μορφή
            # 1.jpg    -> fallback

            filename_bases = [
                f"{int_number:03d}",
                f"{int_number:02d}",
                str(int_number),
            ]

        except Exception:

            filename_bases = [
                str(number)
            ]

    # --------------------------------------------------------
    # ΠΙΘΑΝΑ IMAGE FORMATS
    # --------------------------------------------------------

    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
    ]

    # --------------------------------------------------------
    # ΕΛΕΓΧΟΣ ΑΡΧΕΙΩΝ
    # --------------------------------------------------------

    for filename_base in filename_bases:

        for extension in extensions:

            filename = (
                filename_base
                + extension
            )

            full_path = (
                folder
                / filename
            )

            if full_path.exists():

                return url_for(
                    "static",
                    filename=(
                        f"covers/"
                        f"{series}/"
                        f"{filename}"
                    ),
                )

    # Δεν υπάρχει local cover.

    return ""


# ============================================================
# HELPER - ΜΕΤΑΤΡΟΠΗ DATA ΣΕ COMICS
# ============================================================

def build_comics(
    original,
    series_slug,
):

    comics = []

    for comic in original:

        number = (
            comic.get(
                "number"
            )
        )

        comics.append(
            {
                "number":
                    number,

                "title":
                    comic.get(
                        "title",
                        "",
                    ),

                "image":
                    get_local_cover(
                        series_slug,
                        number,
                    ),

                "owned":
                    comic.get(
                        "owned",
                        False,
                    ),

                "search_title":
                    comic.get(
                        "search_title",
                        "",
                    ),
            }
        )

    return comics


# ============================================================
# ΑΣΤΕΡΙΞ
# ============================================================

def get_asterix_comics():

    comics = []

    for number, title in enumerate(
        ASTERIX_TITLES,
        start=1,
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
                        number,
                    ),

                "owned":
                    False,
            }
        )

    return comics


# ============================================================
# ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

def get_lucky_luke_comics():

    return build_comics(
        load_lucky_luke_comics(),
        "lucky-luke",
    )


# ============================================================
# ΙΝΤΕΦΙΞ
# ============================================================

def get_idefix_comics():

    return build_comics(
        load_idefix_comics(),
        "idefix",
    )


# ============================================================
# ΙΖΝΟΓΚΟΥΝΤ
# ============================================================

def get_iznogoud_comics():

    return build_comics(
        load_iznogoud_comics(),
        "iznogoud",
    )


# ============================================================
# ΡΑΝΤΑΝΠΛΑΝ
# ============================================================

def get_rantanplan_comics():

    return build_comics(
        load_rantanplan_comics(),
        "rantanplan",
    )


# ============================================================
# ΣΕΡΛΟΚ ΧΟΛΜΣ
# ============================================================

def get_sherlock_holmes_comics():

    return build_comics(
        load_sherlock_holmes_comics(),
        "sherlock-holmes",
    )


# ============================================================
# ΑΡΚΑΣ
# ============================================================

def get_arkas_comics():

    return build_comics(
        load_arkas_comics(),
        "arkas",
    )


# ============================================================
# ZELDA
# ============================================================

def get_zelda_comics():

    return build_comics(
        load_zelda_comics(),
        "zelda",
    )


# ============================================================
# DC COMICS
# ============================================================

def get_dc_comics():

    return build_comics(
        load_dc_comics(),
        "dc-comics",
    )


# ============================================================
# MARVEL
# ============================================================

def get_marvel_comics():

    return build_comics(
        load_marvel_comics(),
        "marvel",
    )


# ============================================================
# MARVEL GRAPHIC NOVEL
# ============================================================

def get_marvel_graphic_novels():

    return build_comics(
        load_marvel_graphic_novels(),
        "marvel-graphic-novel",
    )


# ============================================================
# GET COMICS
# ============================================================

def get_comics(
    slug
):

    if slug == "arkas":

        return (
            get_arkas_comics()
        )

    if slug == "lucky-luke":

        return (
            get_lucky_luke_comics()
        )

    if slug == "asterix":

        return (
            get_asterix_comics()
        )

    if slug == "idefix":

        return (
            get_idefix_comics()
        )

    if slug == "iznogoud":

        return (
            get_iznogoud_comics()
        )

    if slug == "rantanplan":

        return (
            get_rantanplan_comics()
        )

    if slug == "sherlock-holmes":

        return (
            get_sherlock_holmes_comics()
        )

    # ========================================================
    # ΝΕΕΣ ΚΑΤΗΓΟΡΙΕΣ
    # ========================================================

    if slug == "zelda":

        return (
            get_zelda_comics()
        )

    if slug == "dc-comics":

        return (
            get_dc_comics()
        )

    if slug == "marvel":

        return (
            get_marvel_comics()
        )

    if slug == "marvel-graphic-novel":

        return (
            get_marvel_graphic_novels()
        )

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

            item = (
                comic.copy()
            )

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
                        category[
                            "slug"
                        ]
                    ),
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
            False,
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
            0,
    }

    return render_template(
        "dashboard.html",

        categories=
            categories,

        stats=
            stats,

        all_comics=
            all_comics,
    )


# ============================================================
# MISSING
# ============================================================

@app.route(
    "/missing"
)
def missing():

    return render_template(
        "missing.html",

        categories=
            categories,

        groups=
            get_comic_groups(),

        all_comics=
            get_all_comics(),
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
        None,
    )

    if selected_category is None:

        return (
            "Η κατηγορία δεν βρέθηκε.",
            404,
        )

    return render_template(
        "category.html",

        category=
            selected_category,

        comics=
            get_comics(
                slug
            ),

        categories=
            categories,
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
    )
