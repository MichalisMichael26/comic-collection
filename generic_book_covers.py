# ============================================================
# GENERIC COVER SERVICE
# Zelda / DC Comics / Marvel / Marvel Graphic Novel
#
# Ψάχνει στο Google Books και επιστρέφει το καλύτερο
# διαθέσιμο cover URL.
# ============================================================

from functools import lru_cache
import re
import unicodedata

import requests


# ============================================================
# GOOGLE BOOKS
# ============================================================

GOOGLE_BOOKS_URL = (
    "https://www.googleapis.com/books/v1/volumes"
)


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),
    "Accept-Language": (
        "en-US,en;q=0.9,el;q=0.8"
    ),
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    text = unicodedata.normalize(
        "NFD",
        str(text or ""),
    )

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    text = text.lower()

    text = re.sub(
        r"[^a-zα-ω0-9]+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# TITLE SCORE
# ============================================================

def title_score(
    query,
    candidate,
):
    query_tokens = set(
        normalize_text(query).split()
    )

    candidate_tokens = set(
        normalize_text(candidate).split()
    )

    if (
        not query_tokens
        or not candidate_tokens
    ):
        return 0

    common = (
        query_tokens
        & candidate_tokens
    )

    return (
        len(common)
        / len(query_tokens)
    )


# ============================================================
# BEST IMAGE
# ============================================================

def best_image_link(
    volume_info,
):
    links = (
        volume_info.get(
            "imageLinks"
        )
        or {}
    )

    for key in (
        "extraLarge",
        "large",
        "medium",
        "small",
        "thumbnail",
        "smallThumbnail",
    ):
        url = links.get(key)

        if not url:
            continue

        url = url.replace(
            "http://",
            "https://",
        )

        # Αφαιρούμε το curl effect
        # που βάζει μερικές φορές
        # το Google Books.
        url = url.replace(
            "&edge=curl",
            "",
        )

        return url

    return None


# ============================================================
# GOOGLE BOOKS COVER SEARCH
# ============================================================

@lru_cache(maxsize=512)
def get_google_books_cover(
    search_title,
):
    if not search_title:
        return None

    try:
        response = requests.get(
            GOOGLE_BOOKS_URL,
            params={
                "q":
                    search_title,

                "maxResults":
                    10,

                "printType":
                    "books",
            },
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        payload = (
            response.json()
        )

    except Exception:
        return None

    items = (
        payload.get(
            "items"
        )
        or []
    )

    if not items:
        return None

    ranked = []

    for item in items:
        info = (
            item.get(
                "volumeInfo"
            )
            or {}
        )

        title = (
            info.get(
                "title"
            )
            or ""
        )

        subtitle = (
            info.get(
                "subtitle"
            )
            or ""
        )

        candidate = (
            f"{title} {subtitle}"
            .strip()
        )

        image = (
            best_image_link(
                info
            )
        )

        if not image:
            continue

        ranked.append(
            (
                title_score(
                    search_title,
                    candidate,
                ),
                image,
            )
        )

    if not ranked:
        return None

    ranked.sort(
        key=lambda item: (
            item[0]
        ),
        reverse=True,
    )

    return ranked[0][1]
