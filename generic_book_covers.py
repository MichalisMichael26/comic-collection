# ============================================================
# GENERIC COMIC / BOOK COVER SEARCH
#
# Sources:
# 1. Open Library
# 2. Google Books
#
# Used by:
# Zelda
# DC Comics
# Marvel
# Marvel Graphic Novel
# ============================================================

from functools import lru_cache
import re
import unicodedata

import requests


# ============================================================
# API URLS
# ============================================================

OPEN_LIBRARY_URL = (
    "https://openlibrary.org/search.json"
)

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
    "Accept": "application/json",
    "Accept-Language": (
        "en-US,en;q=0.9,el;q=0.8"
    ),
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text):

    text = str(
        text or ""
    )

    text = unicodedata.normalize(
        "NFD",
        text,
    )

    text = "".join(
        char
        for char in text
        if unicodedata.category(char)
        != "Mn"
    )

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9α-ω]+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# LATIN-ONLY QUERY
# ============================================================

def latin_query(text):

    text = normalize_text(
        text
    )

    # Κρατάμε αγγλικά / αριθμούς.
    text = re.sub(
        r"[^a-z0-9 ]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# SCORE
# ============================================================

def title_score(
    query,
    candidate,
):

    query_tokens = set(
        latin_query(
            query
        ).split()
    )

    candidate_tokens = set(
        latin_query(
            candidate
        ).split()
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
# QUERY VARIATIONS
# ============================================================

def build_queries(
    search_title,
):

    raw = str(
        search_title or ""
    ).strip()

    latin = (
        latin_query(
            raw
        )
    )

    queries = []

    if raw:
        queries.append(
            raw
        )

    if (
        latin
        and latin not in queries
    ):
        queries.append(
            latin
        )

    # Αφαιρούμε γενικούς όρους
    # που μερικές φορές χαλάνε
    # την αναζήτηση.

    simpler = latin

    remove_terms = [
        "marvel graphic novel collection",
        "graphic novel collection",
        "dc comics",
        "marvel comics",
        "marvel",
        "graphic novel",
    ]

    for term in remove_terms:

        simpler = (
            simpler.replace(
                term,
                " ",
            )
        )

    simpler = re.sub(
        r"\s+",
        " ",
        simpler,
    ).strip()

    if (
        simpler
        and simpler not in queries
    ):
        queries.append(
            simpler
        )

    return queries


# ============================================================
# OPEN LIBRARY
# ============================================================

def get_open_library_cover(
    search_title,
):

    queries = (
        build_queries(
            search_title
        )
    )

    for query in queries:

        try:

            response = requests.get(
                OPEN_LIBRARY_URL,
                params={
                    "q": query,
                    "limit": 10,
                },
                headers=HEADERS,
                timeout=20,
            )

            if response.status_code != 200:

                print(
                    "OpenLibrary HTTP",
                    response.status_code,
                    "for:",
                    query,
                )

                continue

            payload = (
                response.json()
            )

        except Exception as error:

            print(
                "OpenLibrary error:",
                error,
            )

            continue

        docs = (
            payload.get(
                "docs"
            )
            or []
        )

        candidates = []

        for doc in docs:

            cover_id = (
                doc.get(
                    "cover_i"
                )
            )

            if not cover_id:
                continue

            title = (
                doc.get(
                    "title"
                )
                or ""
            )

            score = (
                title_score(
                    search_title,
                    title,
                )
            )

            candidates.append(
                (
                    score,
                    cover_id,
                    title,
                )
            )

        if not candidates:
            continue

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        best = (
            candidates[0]
        )

        cover_id = (
            best[1]
        )

        return (
            "https://covers.openlibrary.org/"
            f"b/id/{cover_id}-L.jpg"
        )

    return None


# ============================================================
# GOOGLE BOOKS IMAGE
# ============================================================

def best_google_image(
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

        url = (
            links.get(
                key
            )
        )

        if not url:
            continue

        url = (
            url.replace(
                "http://",
                "https://",
            )
        )

        url = (
            url.replace(
                "&edge=curl",
                "",
            )
        )

        return url

    return None


# ============================================================
# GOOGLE BOOKS
# ============================================================

def get_google_books_only_cover(
    search_title,
):

    queries = (
        build_queries(
            search_title
        )
    )

    for query in queries:

        try:

            response = requests.get(
                GOOGLE_BOOKS_URL,
                params={
                    "q": query,
                    "maxResults": 10,
                    "printType": "books",
                },
                headers=HEADERS,
                timeout=20,
            )

            if response.status_code != 200:

                print(
                    "Google Books HTTP",
                    response.status_code,
                    "for:",
                    query,
                )

                continue

            payload = (
                response.json()
            )

        except Exception as error:

            print(
                "Google Books error:",
                error,
            )

            continue

        items = (
            payload.get(
                "items"
            )
            or []
        )

        candidates = []

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

            candidate_title = (
                f"{title} {subtitle}"
                .strip()
            )

            image = (
                best_google_image(
                    info
                )
            )

            if not image:
                continue

            score = (
                title_score(
                    search_title,
                    candidate_title,
                )
            )

            candidates.append(
                (
                    score,
                    image,
                )
            )

        if not candidates:
            continue

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return (
            candidates[0][1]
        )

    return None


# ============================================================
# MAIN COVER GETTER
# ============================================================

@lru_cache(
    maxsize=1024
)
def get_google_books_cover(
    search_title,
):

    if not search_title:
        return None

    # --------------------------------------------------------
    # 1. OPEN LIBRARY
    # --------------------------------------------------------

    cover = (
        get_open_library_cover(
            search_title
        )
    )

    if cover:
        return cover

    # --------------------------------------------------------
    # 2. GOOGLE BOOKS
    # --------------------------------------------------------

    cover = (
        get_google_books_only_cover(
            search_title
        )
    )

    if cover:
        return cover

    return None
