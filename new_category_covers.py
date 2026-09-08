# ============================================================
# COVER GETTERS ΓΙΑ ΤΙΣ ΝΕΕΣ ΚΑΤΗΓΟΡΙΕΣ
#
# Zelda
# DC Comics
# Marvel
# Marvel Graphic Novel
# ============================================================

from functools import lru_cache

from generic_book_covers import (
    get_google_books_cover,
)

from zelda_data import (
    ZELDA_COMICS,
)

from dc_comics_data import (
    DC_COMICS,
)

from marvel_data import (
    MARVEL_COMICS,
)

from marvel_graphic_novel_data import (
    MARVEL_GRAPHIC_NOVELS,
)


# ============================================================
# ΒΡΙΣΚΕΙ ΤΟ SEARCH TITLE ΜΕ ΒΑΣΗ ΤΟ NUMBER
# ============================================================

def _find_search_title(
    items,
    number,
):
    try:
        number = int(number)

    except (
        TypeError,
        ValueError,
    ):
        return None

    for item in items:

        try:
            item_number = int(
                item.get(
                    "number",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

        if item_number == number:

            return (
                item.get(
                    "search_title"
                )
                or item.get(
                    "title"
                )
            )

    return None


# ============================================================
# ZELDA
# ============================================================

@lru_cache(
    maxsize=64
)
def get_zelda_cover(
    number,
):
    search_title = (
        _find_search_title(
            ZELDA_COMICS,
            number,
        )
    )

    return (
        get_google_books_cover(
            search_title
        )
    )


# ============================================================
# DC COMICS
# ============================================================

@lru_cache(
    maxsize=128
)
def get_dc_comics_cover(
    number,
):
    search_title = (
        _find_search_title(
            DC_COMICS,
            number,
        )
    )

    return (
        get_google_books_cover(
            search_title
        )
    )


# ============================================================
# MARVEL
# ============================================================

@lru_cache(
    maxsize=128
)
def get_marvel_cover(
    number,
):
    search_title = (
        _find_search_title(
            MARVEL_COMICS,
            number,
        )
    )

    return (
        get_google_books_cover(
            search_title
        )
    )


# ============================================================
# MARVEL GRAPHIC NOVEL
# ============================================================

@lru_cache(
    maxsize=256
)
def get_marvel_graphic_novel_cover(
    number,
):
    search_title = (
        _find_search_title(
            MARVEL_GRAPHIC_NOVELS,
            number,
        )
    )

    return (
        get_google_books_cover(
            search_title
        )
    )
