from flask import Flask, render_template

app = Flask(__name__)

categories = [
    {
        "name": "Αρκάς",
        "slug": "arkas",
        "image": "arkas.jpg"
    },
    {
        "name": "Λούκυ Λουκ",
        "slug": "lucky-luke",
        "image": "lucky_luke.jpg"
    },
    {
        "name": "Αστερίξ",
        "slug": "asterix",
        "image": "asterix.jpg"
    },
    {
        "name": "Ιντεφίξ",
        "slug": "idefix",
        "image": "idefix.jpg"
    }
]


@app.route("/")
def dashboard():
    stats = {
        "total": 0,
        "owned": 0,
        "wishlist": 0,
        "duplicates": 0
    }

    return render_template(
        "dashboard.html",
        categories=categories,
        stats=stats
    )


@app.route("/category/<slug>")
def category(slug):
    selected_category = next(
        (category for category in categories if category["slug"] == slug),
        None
    )

    if selected_category is None:
        return "Η κατηγορία δεν βρέθηκε.", 404

    return render_template(
        "category.html",
        category=selected_category,
        comics=[]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
