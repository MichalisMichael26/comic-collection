from flask import Flask, render_template

app = Flask(__name__)


# --------------------------------------------------
# ΚΑΤΗΓΟΡΙΕΣ
# --------------------------------------------------

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


# --------------------------------------------------
# ΚΟΜΙΚΣ
# --------------------------------------------------

comics_data = {

    "asterix": [

        {
            "number": 1,
            "title": "Ο Αγώνας των Αρχηγών",
            "image": "https://comicstrip.gr/image/catalog/product/asterix-01%3A-o-agwnas-twn-arxhgwn-1.png",
            "status": "none"
        },

        {
            "number": 2,
            "title": "Οβελίξ & ΣΙΑ",
            "image": "https://comicstrip.gr/image/catalog/product/asterix-02%3A-obelix-sia.png",
            "status": "none"
        },

        {
            "number": 3,
            "title": "Ο Αστερίξ στην Ισπανία",
            "image": "https://external.webstorage.gr/mmimages/image/63/67/60/10/0172933-PUBLISHER-BOOK-hero-800x800.jpg",
            "status": "none"
        }

    ],

    "lucky-luke": [],

    "arkas": [],

    "idefix": []
}


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/")
def dashboard():

    all_comics = []

    for series_comics in comics_data.values():
        all_comics.extend(series_comics)

    stats = {
        "total": len(all_comics),

        "owned": sum(
            1 for comic in all_comics
            if comic["status"] == "owned"
        ),

        "wishlist": sum(
            1 for comic in all_comics
            if comic["status"] == "wishlist"
        ),

        "duplicates": sum(
            1 for comic in all_comics
            if comic["status"] == "duplicate"
        )
    }

    return render_template(
        "dashboard.html",
        categories=categories,
        stats=stats
    )


# --------------------------------------------------
# ΚΑΤΗΓΟΡΙΑ
# --------------------------------------------------

@app.route("/category/<slug>")
def category(slug):

    selected_category = next(
        (
            category
            for category in categories
            if category["slug"] == slug
        ),
        None
    )

    if selected_category is None:
        return "Η κατηγορία δεν βρέθηκε.", 404

    comics = comics_data.get(slug, [])

    return render_template(
        "category.html",
        category=selected_category,
        comics=comics
    )


# --------------------------------------------------
# START APP
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
