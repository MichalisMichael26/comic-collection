# ============================================================
# DOWNLOAD ALL COMIC COVERS
#
# Κατεβάζει όλα τα covers και τα αποθηκεύει:
#
# static/covers/lucky-luke/
# static/covers/asterix/
# static/covers/idefix/
# static/covers/iznogoud/
# static/covers/rantanplan/
# static/covers/sherlock-holmes/
# static/covers/arkas/
# static/covers/zelda/
# static/covers/dc-comics/
# static/covers/marvel/
# static/covers/marvel-graphic-novel/
#
# Δημιουργεί επίσης:
# static/covers/manifest.json
# ============================================================

from pathlib import Path
from datetime import datetime, timezone

import json
import time
import requests


# ============================================================
# ΠΑΛΙΑ COVER SERVICES
# ============================================================

from lucky_luke_covers import (
    get_lucky_luke_cover,
    get_lucky_luke_special_cover,
)

from asterix_covers import (
    get_asterix_cover,
)

from idefix_covers import (
    get_idefix_cover,
)

from iznogoud_covers import (
    get_iznogoud_cover,
)

from rantanplan_covers import (
    get_rantanplan_cover,
)

from sherlock_holmes_covers import (
    get_sherlock_holmes_cover,
)

from arkas_covers import (
    get_arkas_cover,
)


# ============================================================
# ΝΕΑ COVER SERVICES
# ============================================================

from new_category_covers import (
    get_zelda_cover,
    get_dc_comics_cover,
    get_marvel_cover,
    get_marvel_graphic_novel_cover,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

COVERS_DIR = (
    BASE_DIR
    / "static"
    / "covers"
)

MANIFEST_FILE = (
    COVERS_DIR
    / "manifest.json"
)


# ============================================================
# REQUEST SETTINGS
# ============================================================

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),

    "Accept": (
        "image/avif,"
        "image/webp,"
        "image/apng,"
        "image/svg+xml,"
        "image/*,"
        "*/*;q=0.8"
    ),

    "Accept-Language": (
        "el-GR,el;q=0.9,en;q=0.8"
    ),
}


# ============================================================
# ΟΛΕΣ ΟΙ ΣΕΙΡΕΣ
# ============================================================

SERIES = {

    # --------------------------------------------------------
    # ΛΟΥΚΥ ΛΟΥΚ
    # --------------------------------------------------------

    "lucky-luke": {
        "name": "Λούκυ Λουκ",
        "count": 90,
        "getter": get_lucky_luke_cover,
    },

    # --------------------------------------------------------
    # ΑΣΤΕΡΙΞ
    # --------------------------------------------------------

    "asterix": {
        "name": "Αστερίξ",
        "count": 41,
        "getter": get_asterix_cover,
    },

    # --------------------------------------------------------
    # ΙΝΤΕΦΙΞ
    # --------------------------------------------------------

    "idefix": {
        "name": "Ιντεφίξ",
        "count": 2,
        "getter": get_idefix_cover,
    },

    # --------------------------------------------------------
    # ΙΖΝΟΓΚΟΥΝΤ
    # --------------------------------------------------------

    "iznogoud": {
        "name": "Ιζνογκούντ",
        "count": 30,
        "getter": get_iznogoud_cover,
    },

    # --------------------------------------------------------
    # ΡΑΝΤΑΝΠΛΑΝ
    # --------------------------------------------------------

    "rantanplan": {
        "name": "Ραντανπλάν",
        "count": 17,
        "getter": get_rantanplan_cover,
    },

    # --------------------------------------------------------
    # ΣΕΡΛΟΚ ΧΟΛΜΣ
    # --------------------------------------------------------

    "sherlock-holmes": {
        "name": "Σέρλοκ Χολμς",
        "count": 4,
        "getter": get_sherlock_holmes_cover,
    },

    # --------------------------------------------------------
    # ΑΡΚΑΣ
    # --------------------------------------------------------

    "arkas": {
        "name": "Αρκάς",
        "count": 27,
        "getter": get_arkas_cover,
    },

    # ========================================================
    # ΝΕΕΣ ΚΑΤΗΓΟΡΙΕΣ
    # ========================================================

    # --------------------------------------------------------
    # ZELDA
    # --------------------------------------------------------

    "zelda": {
        "name": "Zelda",
        "count": 4,
        "getter": get_zelda_cover,
    },

    # --------------------------------------------------------
    # DC COMICS
    # --------------------------------------------------------

    "dc-comics": {
        "name": "DC Comics",
        "count": 16,
        "getter": get_dc_comics_cover,
    },

    # --------------------------------------------------------
    # MARVEL
    # --------------------------------------------------------

    "marvel": {
        "name": "Marvel",
        "count": 14,
        "getter": get_marvel_cover,
    },

    # --------------------------------------------------------
    # MARVEL GRAPHIC NOVEL
    # --------------------------------------------------------

    "marvel-graphic-novel": {
        "name": "Marvel Graphic Novel",
        "count": 120,
        "getter": get_marvel_graphic_novel_cover,
    },
}


# ============================================================
# CONTENT TYPE -> EXTENSION
# ============================================================

CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


# ============================================================
# HEADERS ΑΝΑ SOURCE
# ============================================================

def get_headers_for_url(url):

    headers = (
        DEFAULT_HEADERS.copy()
    )

    if not url:
        return headers

    if "comicstrip.gr" in url:

        headers["Referer"] = (
            "https://comicstrip.gr/"
        )

    elif "comicon-shop.gr" in url:

        headers["Referer"] = (
            "https://comicon-shop.gr/"
        )

    elif "mamouthcomix" in url:

        headers["Referer"] = (
            "https://mamouthcomix-eshop.gr/"
        )

    elif "efantasy.gr" in url:

        headers["Referer"] = (
            "https://www.efantasy.gr/"
        )

    elif "patakis.gr" in url:

        headers["Referer"] = (
            "https://www.patakis.gr/"
        )

    elif "webstorage.gr" in url:

        headers["Referer"] = (
            "https://www.public.gr/"
        )

    elif "scdn.gr" in url:

        headers["Referer"] = (
            "https://www.skroutz.gr/"
        )

    elif "ebayimg.com" in url:

        headers["Referer"] = (
            "https://www.ebay.com/"
        )

    elif "vendora.gr" in url:

        headers["Referer"] = (
            "https://vendora.gr/"
        )

    return headers


# ============================================================
# ΔΙΑΓΡΑΦΗ ΠΑΛΙΩΝ FILES
# ============================================================

def remove_old_issue_files(
    folder,
    filename_base,
):

    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
    ]

    for extension in extensions:

        old_file = (
            folder
            / f"{filename_base}{extension}"
        )

        if old_file.exists():

            try:
                old_file.unlink()

            except Exception:
                pass


# ============================================================
# DOWNLOAD IMAGE
# ============================================================

def download_image(
    image_url,
    folder,
    filename_base,
):

    if not image_url:

        return (
            None,
            "Δεν βρέθηκε URL",
        )

    try:

        response = requests.get(
            image_url,
            headers=get_headers_for_url(
                image_url
            ),
            timeout=25,
            allow_redirects=True,
        )

    except Exception as error:

        return (
            None,
            f"Request error: {error}",
        )

    if response.status_code != 200:

        return (
            None,
            (
                "HTTP "
                f"{response.status_code}"
            ),
        )

    content_type = (
        response.headers
        .get(
            "Content-Type",
            "",
        )
        .split(";")[0]
        .strip()
        .lower()
    )

    extension = (
        CONTENT_TYPE_EXTENSIONS
        .get(
            content_type
        )
    )

    if not extension:

        return (
            None,
            (
                "Δεν είναι "
                "υποστηριζόμενη εικόνα: "
                f"{content_type}"
            ),
        )

    # --------------------------------------------------------
    # Αποφεύγουμε μικρά placeholders / error images
    # --------------------------------------------------------

    if len(response.content) < 3000:

        return (
            None,
            (
                "Πολύ μικρό αρχείο: "
                f"{len(response.content)} bytes"
            ),
        )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    remove_old_issue_files(
        folder,
        filename_base,
    )

    destination = (
        folder
        / f"{filename_base}{extension}"
    )

    try:

        destination.write_bytes(
            response.content
        )

    except Exception as error:

        return (
            None,
            f"Save error: {error}",
        )

    relative_path = (
        destination
        .relative_to(
            BASE_DIR
        )
        .as_posix()
    )

    return (
        "/" + relative_path,
        None,
    )


# ============================================================
# DOWNLOAD SERIES
# ============================================================

def download_series(
    slug,
    data,
    manifest,
):

    name = data["name"]

    count = data["count"]

    getter = data["getter"]

    folder = (
        COVERS_DIR
        / slug
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest["covers"][
        slug
    ] = {}

    manifest["missing"][
        slug
    ] = []

    print()

    print(
        "=" * 60
    )

    print(
        f"{name} - {count} covers"
    )

    print(
        "=" * 60
    )

    for number in range(
        1,
        count + 1,
    ):

        print(
            f"[{slug}] "
            f"{number:03d}/{count:03d}",
            end=" ",
        )

        # ----------------------------------------------------
        # ΒΡΙΣΚΟΥΜΕ URL
        # ----------------------------------------------------

        try:

            image_url = getter(
                number
            )

        except Exception as error:

            image_url = None

            print(
                f"❌ getter error: {error}"
            )

        if not image_url:

            manifest["missing"][
                slug
            ].append(
                {
                    "number":
                        number,

                    "reason":
                        "Δεν βρέθηκε image URL",
                }
            )

            print(
                "❌ URL NOT FOUND"
            )

            # Μικρό delay κυρίως για Google Books
            time.sleep(
                0.20
            )

            continue

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        local_path, error = (
            download_image(
                image_url,
                folder,
                f"{number:03d}",
            )
        )

        if error:

            manifest["missing"][
                slug
            ].append(
                {
                    "number":
                        number,

                    "reason":
                        error,

                    "source":
                        image_url,
                }
            )

            print(
                f"❌ {error}"
            )

            time.sleep(
                0.20
            )

            continue

        manifest["covers"][
            slug
        ][
            str(number)
        ] = {
            "path":
                local_path,

            "source":
                image_url,
        }

        print(
            f"✅ {local_path}"
        )

        # ----------------------------------------------------
        # Μικρό delay για να μην κάνουμε συνεχόμενα requests
        # ----------------------------------------------------

        time.sleep(
            0.20
        )


# ============================================================
# LUCKY LUKE SPECIAL
# ============================================================

def download_lucky_luke_special(
    manifest,
):

    print()

    print(
        "[lucky-luke] SPECIAL",
        end=" ",
    )

    try:

        image_url = (
            get_lucky_luke_special_cover()
        )

    except Exception as error:

        image_url = None

        print(
            f"❌ getter error: {error}"
        )

    if not image_url:

        manifest["missing"][
            "lucky-luke"
        ].append(
            {
                "number":
                    "SPECIAL",

                "reason":
                    "Δεν βρέθηκε image URL",
            }
        )

        print(
            "❌ URL NOT FOUND"
        )

        return

    folder = (
        COVERS_DIR
        / "lucky-luke"
    )

    local_path, error = (
        download_image(
            image_url,
            folder,
            "special",
        )
    )

    if error:

        manifest["missing"][
            "lucky-luke"
        ].append(
            {
                "number":
                    "SPECIAL",

                "reason":
                    error,

                "source":
                    image_url,
            }
        )

        print(
            f"❌ {error}"
        )

        return

    manifest["covers"][
        "lucky-luke"
    ][
        "SPECIAL"
    ] = {
        "path":
            local_path,

        "source":
            image_url,
    }

    print(
        f"✅ {local_path}"
    )


# ============================================================
# SUMMARY
# ============================================================

def print_summary(
    manifest,
):

    print()
    print()

    print(
        "=" * 60
    )

    print(
        "ΤΕΛΙΚΟ ΑΠΟΤΕΛΕΣΜΑ"
    )

    print(
        "=" * 60
    )

    total_ok = 0

    total_missing = 0

    for slug, data in SERIES.items():

        ok = len(
            manifest["covers"]
            .get(
                slug,
                {},
            )
        )

        missing = len(
            manifest["missing"]
            .get(
                slug,
                [],
            )
        )

        total_ok += ok

        total_missing += missing

        print(
            f"{data['name']}: "
            f"✅ {ok} | "
            f"❌ {missing}"
        )

    print(
        "-" * 60
    )

    print(
        f"ΣΥΝΟΛΟ: "
        f"✅ {total_ok} | "
        f"❌ {total_missing}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    COVERS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = {

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "covers":
            {},

        "missing":
            {},
    }

    # --------------------------------------------------------
    # DOWNLOAD ΟΛΩΝ ΤΩΝ SERIES
    # --------------------------------------------------------

    for slug, data in SERIES.items():

        download_series(
            slug,
            data,
            manifest,
        )

    # --------------------------------------------------------
    # SPECIAL LUCKY LUKE
    # --------------------------------------------------------

    download_lucky_luke_special(
        manifest
    )

    # --------------------------------------------------------
    # SAVE MANIFEST
    # --------------------------------------------------------

    MANIFEST_FILE.write_text(

        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=4,
        ),

        encoding="utf-8",
    )

    print_summary(
        manifest
    )

    print()

    print(
        "Manifest:"
    )

    print(
        MANIFEST_FILE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
