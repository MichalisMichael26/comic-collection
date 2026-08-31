from flask import Flask, render_template

from lucky_luke_data import get_lucky_luke_comics
from idefix_data import get_idefix_comics


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
# ΑΣΤΕΡΙΞ - 41 ΤΕΥΧΗ
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
    "Ο Αστερίξ στη Λουζιτανία"

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
                "image": ""
            }
        )

    return comics


# ============================================================
# ΛΟΥΚΥ ΛΟΥΚ
# ============================================================

def get_lucky_luke_without_images():

    original_comics = get_lucky_luke_comics()

    comics = []

    for comic in original_comics:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": ""
            }
        )

    return comics


# ============================================================
# ΙΝΤΕΦΙΞ
# ============================================================

def get_idefix_without_images():

    original_comics = get_idefix_comics()

    comics = []

    for comic in original_comics:

        comics.append(
            {
                "number": comic["number"],
                "title": comic["title"],
                "image": ""
            }
        )

    return comics


# ============================================================
# ΚΟΜΙΚΣ ΑΝΑ ΚΑΤΗΓΟΡΙΑ
# ============================================================

def get_comics(slug):

    if slug == "asterix":

        return get_asterix_comics()


    if slug == "lucky-luke":

        return get_lucky_luke_without_images()


    if slug == "idefix":

        return get_idefix_without_images()


    if slug == "arkas":

        return []


    return []


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    total = (
        len(get_asterix_comics())
        +
        len(get_lucky_luke_comics())
        +
        len(get_idefix_comics())
    )


    stats = {

        "total": total,

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

@app.route("/category/<slug>")
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


    comics = get_comics(slug)


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
