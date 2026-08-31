# ============================================================
# LUCKY LUKE - STATIC COVER URLS
# Χωρίς scraping
# ============================================================


LUCKY_LUKE_COVERS = {

    1: (
        "https://mamouthcomix-eshop.gr/"
        "wp-content/uploads/2022/07/"
        "%CE%BB%CE%BB-01.png"
    ),

    2: (
        "https://cdn.slidesharecdn.com/"
        "ss_thumbnails/"
        "02-230414110324-cc954bd8-thumbnail.jpg"
        "?fit=bounds&height=640&width=640"
    ),

    5: (
        "https://i.ebayimg.com/"
        "images/g/-qwAAOSwEeFVDLef/"
        "s-l1200.jpg"
    ),

    6: (
        "https://bcdn.vendora.gr/"
        "0/4b/92/"
        "4b924e5a4cfe0ba9c2a4182ca0e61e1eae7977d2.jpg"
        "?class=lsq"
    ),

    33: (
        "https://comicstrip.gr/"
        "image/catalog/product/"
        "lucky-luke-33-h-e3agora-twn-ntalton.jpg"
    )

}


# ============================================================
# ΑΡΙΘΜΗΜΕΝΟ ΤΕΥΧΟΣ
# ============================================================

def get_lucky_luke_cover(number):

    return LUCKY_LUKE_COVERS.get(number)


# ============================================================
# SPECIAL
# ============================================================

def get_lucky_luke_special_cover():

    return None
