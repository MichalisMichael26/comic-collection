from functools import lru_cache

from generic_book_covers import get_google_books_cover

from zelda_data import ZELDA_COMICS
from dc_comics_data import DC_COMICS
from marvel_data import MARVEL_COMICS
from marvel_graphic_novel_data import MARVEL_GRAPHIC_NOVELS


def _find_item(items, number):
    try:
        number = int(number)
    except (TypeError, ValueError):
        return None

    for item in items:
        try:
            item_number = int(item.get("number", 0))
        except (TypeError, ValueError):
            continue

        if item_number == number:
            return item

    return None


def _get_cover(items, number):
    item = _find_item(items, number)

    if not item:
        return None

    # Αν έχουμε έτοιμο direct URL, το χρησιμοποιούμε.
    image_url = str(
        item.get("image_url") or ""
    ).strip()

    if image_url:
        return image_url

    # Αν το πεδίο image περιέχει URL, το χρησιμοποιούμε επίσης.
    image = str(
        item.get("image") or ""
    ).strip()

    if image.startswith("http://") or image.startswith("https://"):
        return image

    # Διαφορετικά ψάχνουμε από τον τίτλο.
    search_title = str(
        item.get("search_title")
        or item.get("title")
        or ""
    ).strip()

    if not search_title:
        return None

    return get_google_books_cover(search_title)


@lru_cache(maxsize=64)
def get_zelda_cover(number):
    return _get_cover(
        ZELDA_COMICS,
        number,
    )


@lru_cache(maxsize=128)
def get_dc_comics_cover(number):
    return _get_cover(
        DC_COMICS,
        number,
    )


@lru_cache(maxsize=128)
def get_marvel_cover(number):
    return _get_cover(
        MARVEL_COMICS,
        number,
    )


@lru_cache(maxsize=256)
def get_marvel_graphic_novel_cover(number):
    return _get_cover(
        MARVEL_GRAPHIC_NOVELS,
        number,
    )
