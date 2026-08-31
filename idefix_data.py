# ============================================================
# ΙΝΤΕΦΙΞ
# ============================================================


IDEFIX_TITLES = [

    "Κανένας οίκτος για τους Λατίνους"

]


def get_idefix_comics():

    comics = []

    for number, title in enumerate(
        IDEFIX_TITLES,
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
